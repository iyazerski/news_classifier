from typing import Union

import joblib
import numpy as np

from news_classifier.worker.configs import ClassificationConfigs


class NewsClassifier:
    def __init__(self, configs: ClassificationConfigs):
        self.configs = configs
        self.model = joblib.load(self.configs.model_path)

    def predict(self, x: Union[str, list[str]], **kwargs) -> list[dict]:
        """ Classify input texts and return formatted result with both predicted labels and probabilities """

        if isinstance(x, str):
            return self.predict([x], **kwargs)

        max_predictions_num = kwargs.get('max_predictions_num', self.configs.max_predictions_num)

        # predict probabilities
        prediction = self.model.predict_proba(x)

        # sort labels by probability (asc)
        sorted_labels = np.argsort(prediction, axis=1)

        result = []
        for i in range(prediction.shape[0]):
            result.append({
                'text': x[i],
                'predictions': [{
                    'label': self.model.classes_[j],
                    'proba': prediction[i, j]
                } for j in sorted_labels[i, ::-1][:max_predictions_num]]
            })

        return result
