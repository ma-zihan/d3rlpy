import argparse
from typing import Dict, Tuple

import d3rlpy

BETA_TABLE: Dict[str, Tuple[float, float]] = {
    "halfcheetah-random": (0.001, 0.1),
    "halfcheetah-medium": (0.001, 0.01),
    "halfcheetah-expert": (0.01, 0.01),
    "halfcheetah-medium-replay": (0.01, 0.001),
    "halfcheetah-full-replay": (0.001, 0.1),
    "hopper-random": (0.001, 0.01),
    "hopper-medium": (0.01, 0.001),
    "hopper-expert": (0.1, 0.001),
    "hopper-medium-expert": (0.1, 0.01),
    "hopper-medium-replay": (0.05, 0.5),
    "hopper-full-replay": (0.01, 0.01),
    "walker2d-random": (0.01, 0.0),
    "walker2d-medium": (0.05, 0.1),
    "walker2d-expert": (0.01, 0.5),
    "walker2d-medium-expert": (0.01, 0.01),
    "walker2d-medium-replay": (0.05, 0.01),
    "walker2d-full-replay": (0.01, 0.01),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="hopper-medium-v0")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--gpu", type=int)
    args = parser.parse_args()

    dataset, env = d3rlpy.datasets.get_dataset(args.dataset)

    # fix seed
    d3rlpy.seed(args.seed)
    d3rlpy.envs.seed_env(env, args.seed)

    # deeper network
    encoder = d3rlpy.models.VectorEncoderFactory([256, 256, 256])

    actor_beta, critic_beta = 0.01, 0.01
    for dataset_name, beta_from_paper in BETA_TABLE.items():
        if dataset_name in args.dataset:
            actor_beta, critic_beta = beta_from_paper
            break

    rebrac = d3rlpy.algos.ReBRACConfig(
        actor_learning_rate=1e-3,
        critic_learning_rate=1e-1,
        batch_size=1024,
        gamma=0.99,
        actor_encoder_factory=encoder,
        critic_encoder_factory=encoder,
        target_smoothing_sigma=0.2,
        target_smoothing_clip=0.5,
        update_actor_interval=2,
        actor_beta=actor_beta,
        critic_beta=critic_beta,
        observation_scaler=d3rlpy.preprocessing.StandardObservationScaler(),
    ).create(device=args.gpu)

    rebrac.fit(
        dataset,
        n_steps=500000,
        n_steps_per_epoch=1000,
        save_interval=10,
        evaluators={"environment": d3rlpy.metrics.EnvironmentEvaluator(env)},
        experiment_name=f"ReBRAC_{args.dataset}_{args.seed}",
    )


if __name__ == "__main__":
    main()
