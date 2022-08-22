from lime import lime_image
import matplotlib.pyplot as plt
from lime.wrappers.scikit_image import SegmentationAlgorithm
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('./assets/best_model.h5')

CLASSES = [
    'beagle', 'cocker_spaniel', 'golden_retriever',
    'maltese', 'pekinese', 'pomeranian', 'poodle',
    'samoyed', 'shih_tzu', 'white_terrier']

def img_preprocess(img_path: str):
    img = tf.io.read_file(img_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.resize(img, [299, 299])
    img = tf.expand_dims(img, axis=0)
    img = tf.keras.applications.xception.preprocess_input(img)
    return img.numpy()


def explain_image(img: np.array, saved_filename: str):
    # print('init')
    explainer = lime_image.LimeImageExplainer(verbose=1, random_state=1)

    segmenter = SegmentationAlgorithm(
        'slic',
        n_segments=100,
        compactnes=1,
        sigma=0.5)

    explanation = explainer.explain_instance(
        img,
        classifier_fn=model.predict,  # 10개 class 확률 반환
        top_labels=2,  # 확률 기준 1위
        num_samples=10,  # sample space
        segmentation_fn=segmenter,  # 분할 알고리즘
        num_features=100,
        random_seed=1)


    ind = explanation.top_labels[0]
    dict_heatmap = dict(explanation.local_exp[ind])

    heatmap = np.vectorize(dict_heatmap.get)(explanation.segments)
    
    plt.axis('off')

    plt.imshow(heatmap, cmap='RdBu')
    plt.savefig(saved_filename, bbox_inches='tight',pad_inches = 0)


