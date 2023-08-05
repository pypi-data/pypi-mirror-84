#!/usr/bin/env python

import os

import click
from click import style
from tabulate import tabulate

from nenucal import __version__
from nenucal import datahandler

from libpipe import worker

t_file = click.Path(exists=True, dir_okay=False)


@click.group()
@click.version_option(__version__)
def main():
    ''' NenuFAR-CD data management utilities ...'''


@main.command('list')
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
def list(obs_ids, config):
    ''' List all obs_ids '''
    dh = datahandler.DataHandler.from_file(config)

    header = ['Obs_id'] + [*dh.get_levels()]
    data = []

    for obs_id in dh.get_obs_ids(obs_ids):
        o = [obs_id]
        for level in dh.get_levels():
            counts = []
            for sw in dh.get_spectral_windows():
                mss = dh.get_ms_path(obs_id, level, sw)
                n_mss = len(mss)
                n_mss_exists = sum([os.path.exists(ms) for ms in mss])
                if n_mss == n_mss_exists:
                    counts.append(style(f'{n_mss}', fg='green'))
                elif n_mss_exists > 0:
                    counts.append(style(f'{n_mss_exists}/{n_mss}', fg='orange'))
                else:
                    counts.append(style(f'0/{n_mss}', fg='red'))
            o.append(','.join(counts))
        data.append(o)

    print(tabulate(data, header))


@main.command('get_obs_ids')
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
def get_obs_ids(obs_ids, config):
    ''' List all obs_ids (without existence check) '''
    dh = datahandler.DataHandler.from_file(config)

    print('\n'.join(dh.get_obs_ids(obs_ids)))


@main.command('get_ms')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--sws', '-s', help='Spectral windows', type=str, default='all')
def get_ms(level, obs_ids, config, sws):
    ''' Return a list of all MS corresponding to given OBS_IDS and SWS '''
    dh = datahandler.DataHandler.from_file(config)

    if sws == 'all':
        sws = dh.get_spectral_windows()
    else:
        sws = [k.upper() for k in sws.split(',')]

    for obs_id in dh.get_obs_ids(obs_ids):
        for sw in sws:
            print(' '.join(dh.get_ms_path(obs_id, level, sw)), end=' ')


@main.command('retrieve')
@click.argument('remote_host', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--dry_run', help='Run in dry mode', is_flag=True)
def retrieve(obs_ids, remote_host, config, dry_run):
    ''' Return a list of all MS corresponding to given OBS_IDS and SWS '''
    dh = datahandler.DataHandler.from_file(config)
    assert remote_host in dh.get_remote_hosts(), f'Remote host {remote_host} needs to be defined in {config}'

    target_level = dh.get_remote_level(remote_host)
    target_host = dh.get_remote_host(remote_host)
    target_password_file = dh.get_remote_password_file(remote_host)

    assert target_level in dh.get_levels(), f'{target_level} data level can be retrieved'

    w = worker.WorkerPool(dh.get_all_hosts(), name='Transfert', max_tasks_per_worker=1, debug=dry_run, dry_run=dry_run)

    for obs_id in dh.get_obs_ids(obs_ids):
        date = obs_id.split('_')[0]
        year = date[:4]
        month = date[4:6]

        remote_path = dh.get_remote_data_path(remote_host).replace('%YEAR%', year).replace('%MONTH%', month)

        for sw in dh.get_spectral_windows():
            files = ' '.join([f'{target_host}:{remote_path}/{obs_id}/SB{sb}.MS' for sb in dh.get_sbs(sw)])
            target = dh.get_dir_path(obs_id, target_level, sw)
            node = dh.get_node(obs_id, sw)

            for i in range(100):
                log_file = f'{target}/transfert_{i}.log'
                if not os.path.exists(log_file):
                    break

            if not os.path.exists(target):
                os.makedirs(target)

            cmd = f'sshpass -f {target_password_file} rsync --progress -v -am {files} {target}'

            w.add(cmd, run_on_host=node, output_file=log_file)

    w.execute()


@main.command('l1_to_l2')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--force', help='Force overwrite data if already exists', is_flag=True)
@click.option('--l1_level', help='L1 level name', type=str, default='L1')
@click.option('--dry_run', help='Do not do anything', is_flag=True)
def l1_to_l2(level, obs_ids, config, force, l1_level, dry_run):
    ''' Create L2 data (at level LEVEL) from L1 data for the given OBS_IDS'''
    dh = datahandler.DataHandler.from_file(config)
    assert 'L1' in dh.get_levels(), f'L1 data level needs to be defined'
    assert level in dh.get_levels(), f'{level} data level needs to be defined'

    dppp_file = dh.get_l1_to_l2_config(level)

    w = worker.WorkerPool(dh.get_all_hosts(), name='L1 to L2', max_tasks_per_worker=1, debug=dry_run, dry_run=dry_run)

    for obs_id in dh.get_obs_ids(obs_ids):
        for sw in dh.get_spectral_windows():
            msins = ','.join(dh.get_ms_path(obs_id, l1_level, sw))
            msout = dh.get_ms_path(obs_id, level, sw)[0]
            target = os.path.dirname(msout)
            node = dh.get_node(obs_id, sw)

            if os.path.exists(msout):
                if force:
                    print(f'Warning: {msout} already exists')
                else:
                    print(f'Error: {msout} already exists')
                    return 1

            if not os.path.exists(target):
                os.makedirs(target)

            for i in range(100):
                log_file = f'{target}/l2_to_l1_{i}.log'
                if not os.path.exists(log_file):
                    break

            print(dppp_file, msins, msout)

            cmd = f'DPPP {os.path.abspath(dppp_file)} msin=[{msins}] msout={msout} msout.overwrite=true'

            w.add(cmd, run_on_host=node, output_file=log_file)

    w.execute()


@main.command('make_ms_list')
@click.argument('level', type=str)
@click.argument('obs_ids', type=str)
@click.option('--config', '-c', help='Data handler configuration file', type=t_file, default='data_handler.toml')
@click.option('--target', help='Target directory', default='ms_lists')
def make_ms_list(level, obs_ids, config, target):
    ''' Make MS list for all OBS_IDS at level LEVEL '''
    dh = datahandler.DataHandler.from_file(config)
    assert level in dh.get_levels(), f'{level} data level needs to be defined'

    if not os.path.exists(target):
        os.makedirs(target)

    for obs_id in dh.get_obs_ids(obs_ids):
        for sw in dh.get_spectral_windows():
            ms = dh.get_ms_path(obs_id, level, sw)[0]
            filepath = os.path.join(target, f'{obs_id}_{level}_{sw}')

            with open(filepath, 'w') as f:
                f.write(f'{ms}\n')
