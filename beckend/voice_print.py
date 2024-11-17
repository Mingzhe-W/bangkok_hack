import numpy as np
import librosa
from sklearn.mixture import GaussianMixture
import os

# Function to extract MFCC features from an audio file
def extract_features(audio_file, n_mfcc=13):
    y, sr = librosa.load(audio_file, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T  # Transpose for proper GMM fitting

# Train a GMM for a given speaker
def train_gmm(feature_vectors, n_components=8):
    gmm = GaussianMixture(n_components=n_components, covariance_type='diag', max_iter=200, random_state=42)
    gmm.fit(feature_vectors)
    return gmm


def save_model(gmm, filename):
    import joblib
    joblib.dump(gmm, filename)


def load_model(filename):
    import joblib
    return joblib.load(filename)


def recognize_speaker(test_features, gmm_models):
    log_likelihoods = []
    for speaker, model in gmm_models.items():
        log_likelihood = model.score(test_features)
        log_likelihoods.append((speaker, log_likelihood))
    # Find the speaker with the highest log likelihood
    recognized_speaker = max(log_likelihoods, key=lambda x: x[1])
    return recognized_speaker


if __name__ == "__main__":
    # Directories for training and testing audio files
    train_dir = "./train_audio/"
    test_file = "./test_audio/test.wav"

    # Train GMM models for each speaker
    gmm_models = {}
    for speaker in os.listdir(train_dir):
        speaker_path = os.path.join(train_dir, speaker)
        if os.path.isdir(speaker_path):
            features = []
            for audio_file in os.listdir(speaker_path):
                file_path = os.path.join(speaker_path, audio_file)
                features.append(extract_features(file_path))
            features = np.vstack(features)
            gmm = train_gmm(features)
            gmm_models[speaker] = gmm
            save_model(gmm, f"{speaker}_gmm.model")

    # Test the recognition system
    test_features = extract_features(test_file)
    recognized_speaker = recognize_speaker(test_features, gmm_models)
    print(f"Recognized Speaker: {recognized_speaker[0]} with log-likelihood: {recognized_speaker[1]}")
