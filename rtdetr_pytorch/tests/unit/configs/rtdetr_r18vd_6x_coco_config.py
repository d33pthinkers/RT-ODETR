from pathlib import Path

from src.core import YAMLConfig


def test_rtdetr_r18vd_6x_coco_yml():
    config_file = Path(
        Path(__file__).parent.parent.parent.parent
        / "configs/rtdetr/rtdetr_r18vd_6x_coco.yml"
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
        "HybridEncoder": {
            "act": "silu",
            "depth_mult": 1,
            "dim_feedforward": 1024,
            "dropout": 0.0,
            "enc_act": "gelu",
            "eval_spatial_size": [640, 640],
            "expansion": 0.5,
            "feat_strides": [8, 16, 32],
            "hidden_dim": 256,
            "in_channels": [128, 256, 512],
            "nhead": 8,
            "num_encoder_layers": 1,
            "pe_temperature": 10000,
            "use_encoder_idx": [2],
        },
        "PResNet": {
            "depth": 18,
            "freeze_at": -1,
            "freeze_norm": False,
            "num_stages": 4,
            "pretrained": True,
            "return_idx": [1, 2, 3],
            "variant": "d",
        },
        "RTDETR": {
            "backbone": "PResNet",
            "decoder": "RTDETRTransformer",
            "encoder": "HybridEncoder",
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
        "RTDETRPostProcessor": {"num_top_queries": 300},
        "RTDETRTransformer": {
            "eval_idx": -1,
            "eval_spatial_size": [640, 640],
            "feat_channels": [256, 256, 256],
            "feat_strides": [8, 16, 32],
            "hidden_dim": 256,
            "num_decoder_layers": 3,
            "num_denoising": 100,
            "num_levels": 3,
            "num_queries": 300,
        },
        "SetCriterion": {
            "alpha": 0.75,
            "gamma": 2.0,
            "losses": ["vfl", "boxes"],
            "matcher": {
                "alpha": 0.25,
                "gamma": 2.0,
                "type": "HungarianMatcher",
                "weight_dict": {"cost_bbox": 5, "cost_class": 2, "cost_giou": 2},
            },
            "weight_dict": {"loss_bbox": 5, "loss_giou": 2, "loss_vfl": 1},
        },
        "__include__": [
            "../dataset/coco_detection.yml",
            "../runtime.yml",
            "./include/dataloader.yml",
            "./include/optimizer.yml",
            "./include/rtdetr_r50vd.yml",
        ],
        "clip_max_norm": 0.1,
        "criterion": "SetCriterion",
        "ema": {"decay": 0.9999, "type": "ModelEMA", "warmups": 2000},
        "epoches": 72,
        "find_unused_parameters": True,
        "lr_scheduler": {"gamma": 0.1, "milestones": [1000], "type": "MultiStepLR"},
        "model": "RTDETR",
        "num_classes": 80,
        "optimizer": {
            "betas": [0.9, 0.999],
            "lr": 0.0001,
            "params": [
                {
                    "lr": 1e-05,
                    "params": "^(?=.*backbone)(?=.*norm).*$",
                    "weight_decay": 0.0,
                },
                {"lr": 1e-05, "params": "^(?=.*backbone)(?!.*norm).*$"},
                {
                    "params": "^(?=.*(?:encoder|decoder))(?=.*(?:norm|bias)).*$",
                    "weight_decay": 0.0,
                },
            ],
            "type": "AdamW",
            "weight_decay": 0.0001,
        },
        "output_dir": "./output/rtdetr_r18vd_6x_coco",
        "postprocessor": "RTDETRPostProcessor",
        "remap_mscoco_category": True,
        "scaler": {"enabled": True, "type": "GradScaler"},
        "sync_bn": True,
        "task": "detection",
        "train_dataloader": {
            "batch_size": 4,
            "collate_fn": "default_collate_fn",
            "dataset": {
                "ann_file": "./dataset/coco/annotations/instances_train2017.json",
                "img_folder": "./dataset/coco/train2017/",
                "return_masks": False,
                "transforms": {
                    "ops": [
                        {"p": 0.8, "type": "RandomPhotometricDistort"},
                        {"fill": 0, "type": "RandomZoomOut"},
                        {"p": 0.8, "type": "RandomIoUCrop"},
                        {"min_size": 1, "type": "SanitizeBoundingBox"},
                        {"type": "RandomHorizontalFlip"},
                        {"size": [640, 640], "type": "Resize"},
                        {"type": "ToImageTensor"},
                        {"type": "ConvertDtype"},
                        {"min_size": 1, "type": "SanitizeBoundingBox"},
                        {"normalize": True, "out_fmt": "cxcywh", "type": "ConvertBox"},
                    ],
                    "type": "Compose",
                },
                "type": "CocoDetection",
            },
            "drop_last": True,
            "num_workers": 4,
            "shuffle": True,
            "type": "DataLoader",
        },
        "use_amp": False,
        "use_ema": True,
        "use_focal_loss": True,
        "val_dataloader": {
            "batch_size": 8,
            "collate_fn": "default_collate_fn",
            "dataset": {
                "ann_file": "./dataset/coco/annotations/instances_val2017.json",
                "img_folder": "./dataset/coco/val2017/",
                "transforms": {
                    "ops": [
                        {"size": [640, 640], "type": "Resize"},
                        {"type": "ToImageTensor"},
                        {"type": "ConvertDtype"},
                    ],
                    "type": "Compose",
                },
                "type": "CocoDetection",
            },
            "drop_last": False,
            "num_workers": 4,
            "shuffle": False,
            "type": "DataLoader",
        },
    }
