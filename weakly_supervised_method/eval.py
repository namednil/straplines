from sklearn.metrics import classification_report, confusion_matrix


def compute_metrics(predictions, labels):
    return classification_report(y_true=labels, y_pred=predictions, labels=[0, 1])


def generate_confusion_matrix(predictions, labels):
    return confusion_matrix(y_true=labels, y_pred=predictions, labels=[0, 1])
