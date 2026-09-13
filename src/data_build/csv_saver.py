import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
def save_scene_table(scene_rows, out_path):
    try:
        df = pd.DataFrame(scene_rows)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
    except Exception as e:
        logger.error(f"Ошибка при сохранении CSV: {e}")
        return

    logger.info(f"Сцены успешно сохранены в {out_path}")
