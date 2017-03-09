import tensorflow as tf

from models.utils.distributions import draw_norm
from models.utils.tf_helpers import create_h_weights, create_z_weights, mlp_neuron


def q_z_given_x(x, hidden_dim, input_dim, latent_dim, reuse=False):
    with tf.variable_scope("encoder_z1", reuse=reuse):
        # Variables
        w_h1, b_h1 = create_h_weights('h1_z1', 'M1_encoder', [input_dim, hidden_dim])
        w_h2, b_h2 = create_h_weights('h2_z1', 'M1_encoder', [hidden_dim, hidden_dim])

        w_mu_z1, w_var_z1, b_mu_z1, b_var_z1 = create_z_weights('z_1', [hidden_dim, latent_dim])

        # Hidden layers
        h1 = mlp_neuron(x, w_h1, b_h1)
        h2 = mlp_neuron(h1, w_h2, b_h2)

        # Z1 latent layer mu and var
        logvar_z1 = mlp_neuron(h2, w_var_z1, b_var_z1, activation=False)
        mu_z1 = mlp_neuron(h2, w_mu_z1, b_mu_z1, activation=False)
        # Model
        z1 = draw_norm(latent_dim, mu_z1, logvar_z1)
        return z1, mu_z1, logvar_z1