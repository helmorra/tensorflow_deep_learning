import matplotlib

matplotlib.use('Agg')
print("matplotlib: %s, %s" % (matplotlib.__version__, matplotlib.__file__))
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from  sklearn.metrics import roc_curve, auc


def convert_labels_to_cls(labels):
    return np.argmax(labels, axis=1)


def cls_accuracy(correct):
    correct_sum = correct.sum()
    acc = float(correct_sum) / len(correct)
    return acc, correct_sum


def plot_confusion_matrix(cls_pred, labels, logging):
    cls_true = convert_labels_to_cls(labels)
    cm = confusion_matrix(y_true=cls_true,
                          y_pred=cls_pred)
    print(cm)
    logging.debug(cm)
    plt.matshow(cm)


def print_test_accuracy(correct, cls_pred, labels, logging):
    acc, correct_sum = cls_accuracy(correct)
    num_images = len(correct)
    msg = "Accuracy on Test-Set: {0:.1%} ({1} / {2})"
    print(msg.format(acc, correct_sum, num_images))
    logging.debug(msg.format(acc, correct_sum, num_images))

    print("Confusion Matrix:")
    logging.debug("Confusion Matrix:")

    # print(tf.confusion_matrix(labels=convert_labels_to_cls(labels), predictions=cls_pred, num_classes=10))
    plot_confusion_matrix(cls_pred=cls_pred, labels=labels, logging=logging)


def plot_roc(logits, y_true, n_classes, name):
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true[:, i], logits[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), logits.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure()
    lw = 2
    plt.plot(fpr[2], tpr[2], color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[2])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    title = 'ROC of ' + name + ' model'
    plt.title(title)
    plt.legend(loc="lower right")
    save_path = name + "ROC"
    plt.savefig(save_path)


def plot_images(x_test, x_reconstruct, n_images, name):
    assert len(x_test) == n_images
    print("x_reconstruct:{}, x_test:{}".format(x_reconstruct.shape, x_test.shape))

    plt.figure(figsize=(8, 12))
    for i in range(n_images):
        # Plot image.
        plt.subplot(n_images, 2, 2 * i + 1)
        s1 = plt.imshow(x_test[i].reshape(28, 28), vmin=0, vmax=1, cmap="gray")
        plt.title("Test input")
        plt.subplot(n_images, 2, 2 * i + 2)
        s2 = plt.imshow(x_reconstruct[i].reshape(28, 28), vmin=0, vmax=1, cmap="gray")
        plt.title("Reconstruction")
        s1.axes.get_xaxis().set_visible(False)
        s1.axes.get_yaxis().set_visible(False)
        s2.axes.get_xaxis().set_visible(False)
        s2.axes.get_yaxis().set_visible(False)

    # plt.title("Left: Test input and Right: Reconstruction")
    plt.tight_layout()
    save_path = name + "_reconstructed_digit"
    plt.savefig(save_path)
    # plt.axis('off')


def plot_cost(training, validation, name, epochs, best_epoch):
    x = np.arange(start=0, stop=len(training), step=1).tolist()
    plt.figure()
    plt.xlim(min(x), max(x))
    plt.ylim(0, max(max(training), max(validation)) + 0.2)
    plt.plot(x, training, color='blue', linestyle='-', label='training')
    plt.plot(x, validation, color='green', linestyle='-', label='validation')
    plt.axvline(x=best_epoch, color='red')
    title = '{}: epochs={}, best_epoch={} '.format(name, epochs, best_epoch)
    plt.title(title)
    plt.xlabel('Iteration')
    plt.legend(loc='best')
    plt.savefig(name)


def plot_line(input_func, name, epochs, best_epoch):
    x = np.arange(start=0, stop=len(input_func), step=1).tolist()
    plt.figure()
    plt.xlim(min(x), max(x))
    plt.plot(x, input_func, color='blue', linestyle='-', label='training')
    plt.axvline(x=best_epoch, color='red')
    title = '{}: epochs={}, best_epoch={} '.format(name, epochs, best_epoch)
    plt.title(title)
    plt.xlabel('Iteration')
    plt.legend(loc='best')
    plt.savefig(name)
