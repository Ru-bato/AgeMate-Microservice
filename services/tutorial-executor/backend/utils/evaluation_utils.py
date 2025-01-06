# -*- coding: utf-8 -*-
"""
Evaluation Utilities

This module contains utility functions for evaluating models, predictions, and other outputs in various applications.
It provides functionalities such as calculating accuracy, precision, recall, F1 score, ROC AUC, MSE, R2, and more advanced metrics.
"""

from typing import List, Dict, Tuple, Any, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    mean_squared_error,
    r2_score
)
import warnings


class EvaluationUtils:
    @staticmethod
    def calculate_accuracy(y_true: List[Any], y_pred: List[Any]) -> float:
        """
        Calculates the accuracy of predictions.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.

        Returns:
            float: The accuracy score.
        """
        return accuracy_score(y_true, y_pred)

    @staticmethod
    def calculate_precision(y_true: List[Any], y_pred: List[Any], average: str = 'binary') -> float:
        """
        Calculates the precision of predictions.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            average (str): The type of averaging to perform ('binary', 'micro', 'macro', etc.).

        Returns:
            float: The precision score.
        """
        return precision_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def calculate_recall(y_true: List[Any], y_pred: List[Any], average: str = 'binary') -> float:
        """
        Calculates the recall of predictions.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            average (str): The type of averaging to perform ('binary', 'micro', 'macro', etc.).

        Returns:
            float: The recall score.
        """
        return recall_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def calculate_f1_score(y_true: List[Any], y_pred: List[Any], average: str = 'binary') -> float:
        """
        Calculates the F1 score of predictions.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            average (str): The type of averaging to perform ('binary', 'micro', 'macro', etc.).

        Returns:
            float: The F1 score.
        """
        return f1_score(y_true, y_pred, average=average, zero_division=0)

    @staticmethod
    def generate_confusion_matrix(y_true: List[Any], y_pred: List[Any], labels: Optional[List[Any]] = None) -> np.ndarray:
        """
        Generates a confusion matrix for the predictions.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            labels (Optional[List[Any]]): The list of labels to index the matrix. Defaults to None.

        Returns:
            np.ndarray: The confusion matrix as a NumPy array.
        """
        return confusion_matrix(y_true, y_pred, labels=labels)

    @staticmethod
    def generate_classification_report(y_true: List[Any], y_pred: List[Any], labels: Optional[List[Any]] = None, target_names: Optional[List[str]] = None) -> str:
        """
        Generates a detailed classification report including precision, recall, F1 score, and support.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            labels (Optional[List[Any]]): The list of labels to index the matrix. Defaults to None.
            target_names (Optional[List[str]]): Optional display names matching the labels. Defaults to None.

        Returns:
            str: A string representation of the classification report.
        """
        return classification_report(y_true, y_pred, labels=labels, target_names=target_names, zero_division=0)

    @staticmethod
    def calculate_roc_auc(y_true: List[Any], y_score: List[Any]) -> float:
        """
        Calculates the ROC AUC score for binary classification.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_score (List[Any]): The predicted probabilities or scores.

        Returns:
            float: The ROC AUC score.
        """
        try:
            return roc_auc_score(y_true, y_score)
        except ValueError as e:
            warnings.warn(f"Failed to calculate ROC AUC due to {e}. Returning NaN.")
            return float('nan')

    @staticmethod
    def calculate_mean_squared_error(y_true: List[float], y_pred: List[float]) -> float:
        """
        Calculates the mean squared error for regression tasks.

        Args:
            y_true (List[float]): The ground truth values.
            y_pred (List[float]): The predicted values.

        Returns:
            float: The mean squared error.
        """
        return mean_squared_error(y_true, y_pred)

    @staticmethod
    def calculate_r2_score(y_true: List[float], y_pred: List[float]) -> float:
        """
        Calculates the R^2 (coefficient of determination) score for regression tasks.

        Args:
            y_true (List[float]): The ground truth values.
            y_pred (List[float]): The predicted values.

        Returns:
            float: The R^2 score.
        """
        return r2_score(y_true, y_pred)

    @staticmethod
    def evaluate_regression(y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """
        Evaluates a regression model using multiple metrics.

        Args:
            y_true (List[float]): The ground truth values.
            y_pred (List[float]): The predicted values.

        Returns:
            Dict[str, float]: A dictionary containing various evaluation metrics.
        """
        mse = EvaluationUtils.calculate_mean_squared_error(y_true, y_pred)
        r2 = EvaluationUtils.calculate_r2_score(y_true, y_pred)
        return {
            'mean_squared_error': mse,
            'r2_score': r2
        }

    @staticmethod
    def evaluate_classification(y_true: List[Any], y_pred: List[Any], average: str = 'binary') -> Dict[str, float]:
        """
        Evaluates a classification model using multiple metrics.

        Args:
            y_true (List[Any]): The ground truth labels.
            y_pred (List[Any]): The predicted labels.
            average (str): The type of averaging to perform ('binary', 'micro', 'macro', etc.).

        Returns:
            Dict[str, float]: A dictionary containing various evaluation metrics.
        """
        accuracy = EvaluationUtils.calculate_accuracy(y_true, y_pred)
        precision = EvaluationUtils.calculate_precision(y_true, y_pred, average=average)
        recall = EvaluationUtils.calculate_recall(y_true, y_pred, average=average)
        f1 = EvaluationUtils.calculate_f1_score(y_true, y_pred, average=average)
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }