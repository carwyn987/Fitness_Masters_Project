import argparse
from src.load import load_and_split

def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Train a segmentation CNN model.')
    # parser.add_argument('--sum', type=int, default=0, help='train')
    args = parser.parse_args()

    # Load Data

    data_folder = '../Skin_Anatomical_Image_Dataset/simple_image_config'
    train, validation, test = load_and_split(data_folder)


if __name__ == "__main__":
    main()