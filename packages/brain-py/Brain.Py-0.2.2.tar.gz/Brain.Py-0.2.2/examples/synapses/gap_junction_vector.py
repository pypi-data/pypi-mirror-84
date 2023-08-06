# -*- coding: utf-8 -*-

import brainpy as bp
import brainpy.numpy as np


def GapJunction():
    requires = dict(
        ST=bp.types.SynState(
            ['s', 'w'],
            help='''
            Gap junction state.

            s : conductance for post-synaptic neuron.
            w : gap junction conductance.
            '''
        ),
        pre=bp.types.NeuState(['V']),
        post=bp.types.NeuState(['V', 'inp']),
        post2syn=bp.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=bp.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    def update(ST, pre, post, post2syn, pre_ids):
        num_post = len(post2syn)
        for post_id in range(num_post):
            for syn_id in post2syn[post_id]:
                pre_id = pre_ids[syn_id]
                post['inp'][post_id] = ST['w'][syn_id] * (pre['V'][pre_id] - post['V'][post_id])

    return bp.SynType(name='GapJunction', requires=requires, steps=update, vector_based=True)


def gap_junction_lif(spikelet=0.1):
    requires = dict(
        ST=bp.types.SynState(
            ['spikelet', 'w'],
            help='''
                Gap junction state.

                s : conductance for post-synaptic neuron.
                w : gap junction conductance. It
                '''
        ),
        pre=bp.types.NeuState(['V', 'sp']),
        post=bp.types.NeuState(['V', 'inp']),
        post2syn=bp.types.ListConn(help='post-to-synapse connection.'),
        pre_ids=bp.types.Array(dim=1, help='Pre-synaptic neuron indices.'),
    )

    def update(ST, pre, post, post2syn, pre_ids):
        num_post = len(post2syn)
        for post_id in range(num_post):
            for syn_id in post2syn[post_id]:
                pre_id = pre_ids[syn_id]
                post['inp'][post_id] += ST['w'] * (pre['V'][pre_id] - post['V'][post_id])
                ST['spikelet'][syn_id] = ST['w'][syn_id] * spikelet * pre['sp']

    @bp.delayed
    def output(ST, post, post2syn):
        post_spikelet = np.zeros(len(post2syn), dtype=np.float_)
        for post_id, syn_ids in enumerate(post2syn):
            post_spikelet[post_id] = np.sum(ST['spikelet'][syn_ids])
        post['V'] += post_spikelet

    return bp.SynType(name='GapJunctin_for_LIF',
                      requires=requires,
                      steps=update,
                      vector_based=True)
