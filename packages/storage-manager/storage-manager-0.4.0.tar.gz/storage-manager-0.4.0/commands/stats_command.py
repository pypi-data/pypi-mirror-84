#  Copyright (c) 2020, Mandar Patil <mandarons@pm.me>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import sys

import click
import humanfriendly
from tabulate import tabulate

from commands import pass_config


@click.group(short_help='Shows various statistics.')
@pass_config
def stats(config):
    pass


def _show_all_stats(config):
    result = config.stats_db.get_all()
    if len(result) == 0:
        config.error('No stats exist.')
        sys.exit(1)
    data = [list(r['stats'].values())[:-1] for r in result]
    for entry in data:
        entry[0] = humanfriendly.format_size(entry[0])
        entry[1] = humanfriendly.format_size(entry[1])
        entry[2] = humanfriendly.format_size(entry[2])
        entry[3] = humanfriendly.format_number(entry[3])
    headers = list(result[0]['stats'])
    headers.remove('items')
    config.info(tabulate(tabular_data=data, headers=headers))


@stats.command(short_help='Shows summary of storage.')
@pass_config
def show_all(config):
    '''
    Summary of storage.
    '''
    config.debug('Showing summary of storage ...')
    _show_all_stats(config=config)
    config.debug('Completed.')
