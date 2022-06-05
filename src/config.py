from typing import Dict, Any

config: dict[Any, Any] = {

    "camera-settings": {
        "highcontrast": {
            "width": 640,
            "brightness": 180,
            "contrast": 255,
            "saturation": 0,
            "gain": 32,
            "exposure": -2,
            "white balance": 1,
        },
        "lowcontrast": {
            "width": 640,
            "brightness": 0,
            "contrast": 0,
            "saturation": 0,
            "gain": 0,
            "exposure": 0,
            "white balance": 1,
        },
    },
    "coins": {
        "1cent": {
            "min": 400,
            "max": 500,
            "color":0,
        },
        "2cent": {
            "min":0,
        },

    }
}
