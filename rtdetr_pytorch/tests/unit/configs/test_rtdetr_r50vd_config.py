from pathlib import Path

from src.core import YAMLConfig


def test_rtdetr_r50vd_yml():
    config_file = Path(
        Path(__file__).parent.parent.parent.parent
        / "configs/rtdetr/include/rtdetr_r50vd.yml"
    ).resolve()
    assert config_file.is_file()
    cfg = YAMLConfig(cfg_path=str(config_file))
    assert cfg
    assert cfg.model.multi_scale == [
        480,
        512,
        544,
        576,
        608,
        640,
        640,
        640,
        672,
        704,
        736,
        768,
        800,
    ]
    assert cfg.yaml_cfg == {
        "task": "detection",
        "model": "RTDETR",
        "criterion": "SetCriterion",
        "postprocessor": "RTDETRPostProcessor",
        "RTDETR": {
            "backbone": "PResNet",
            "encoder": "HybridEncoder",
            "decoder": "RTDETRTransformer",
            "multi_scale": [
                480,
                512,
                544,
                576,
                608,
                640,
                640,
                640,
                672,
                704,
                736,
                768,
                800,
            ],
        },
        "PResNet": {
            "depth": 50,
            "variant": "d",
            "freeze_at": 0,
            "return_idx": [1, 2, 3],
            "num_stages": 4,
            "freeze_norm": True,
            "pretrained": True,
        },
        "HybridEncoder": {
            "in_channels": [512, 1024, 2048],
            "feat_strides": [8, 16, 32],
            "hidden_dim": 256,
            "use_encoder_idx": [2],
            "num_encoder_layers": 1,
            "nhead": 8,
            "dim_feedforward": 1024,
            "dropout": 0.0,
            "enc_act": "gelu",
            "pe_temperature": 10000,
            "expansion": 1.0,
            "depth_mult": 1,
            "act": "silu",
            "eval_spatial_size": [640, 640],
        },
        "RTDETRTransformer": {
            "feat_channels": [256, 256, 256],
            "feat_strides": [8, 16, 32],
            "hidden_dim": 256,
            "num_levels": 3,
            "num_queries": 300,
            "num_decoder_layers": 6,
            "num_denoising": 100,
            "eval_idx": -1,
            "eval_spatial_size": [640, 640],
        },
        "use_focal_loss": True,
        "RTDETRPostProcessor": {"num_top_queries": 300},
        "SetCriterion": {
            "weight_dict": {"loss_vfl": 1, "loss_bbox": 5, "loss_giou": 2},
            "losses": ["vfl", "boxes"],
            "alpha": 0.75,
            "gamma": 2.0,
            "matcher": {
                "type": "HungarianMatcher",
                "weight_dict": {"cost_class": 2, "cost_bbox": 5, "cost_giou": 2},
                "alpha": 0.25,
                "gamma": 2.0,
            },
        },
    }
