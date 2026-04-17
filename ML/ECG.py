from skimage.io import imread
from skimage import color
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, gaussian
from skimage.transform import resize
from skimage import measure
from sklearn.preprocessing import MinMaxScaler
import joblib
import pandas as pd
import numpy as np
import os
from natsort import natsorted


class ECG:

    def getImage(self, image):
        return imread(image)

    def GrayImgae(self, image):
        image_gray = color.rgb2gray(image)
        image_gray = resize(image_gray, (1572, 2213))
        return image_gray

    def DividingLeads(self, image):

        Lead_1 = image[300:600, 150:643]
        Lead_2 = image[300:600, 646:1135]
        Lead_3 = image[300:600, 1140:1625]
        Lead_4 = image[300:600, 1630:2125]
        Lead_5 = image[600:900, 150:643]
        Lead_6 = image[600:900, 646:1135]
        Lead_7 = image[600:900, 1140:1625]
        Lead_8 = image[600:900, 1630:2125]
        Lead_9 = image[900:1200, 150:643]
        Lead_10 = image[900:1200, 646:1135]
        Lead_11 = image[900:1200, 1140:1625]
        Lead_12 = image[900:1200, 1630:2125]
        Lead_13 = image[1250:1480, 150:2125]

        Leads = [Lead_1, Lead_2, Lead_3, Lead_4, Lead_5, Lead_6,
                 Lead_7, Lead_8, Lead_9, Lead_10, Lead_11, Lead_12, Lead_13]

        fig, ax = plt.subplots(4, 3)
        fig.set_size_inches(10, 10)

        x_counter = 0
        y_counter = 0

        for x, y in enumerate(Leads[:-1]):
            ax[x_counter][y_counter].imshow(y)
            ax[x_counter][y_counter].axis('off')
            ax[x_counter][y_counter].set_title(f"Leads {x+1}")

            if (x + 1) % 3 == 0:
                x_counter += 1
                y_counter = 0
            else:
                y_counter += 1

        fig.savefig('Leads_1-12_figure.png')

        fig1, ax1 = plt.subplots()
        fig1.set_size_inches(10, 10)
        ax1.imshow(Lead_13)
        ax1.set_title("Leads 13")
        ax1.axis('off')
        fig1.savefig('Long_Lead_13_figure.png')

        return Leads

    def PreprocessingLeads(self, Leads):

        fig2, ax2 = plt.subplots(4, 3)
        fig2.set_size_inches(10, 10)

        x_counter = 0
        y_counter = 0

        for x, y in enumerate(Leads[:-1]):
            grayscale = color.rgb2gray(y)
            blurred = gaussian(grayscale, sigma=1)
            thresh = threshold_otsu(blurred)
            binary = resize(blurred < thresh, (300, 450))

            ax2[x_counter][y_counter].imshow(binary, cmap="gray")
            ax2[x_counter][y_counter].axis('off')
            ax2[x_counter][y_counter].set_title(f"Lead {x+1}")

            if (x + 1) % 3 == 0:
                x_counter += 1
                y_counter = 0
            else:
                y_counter += 1

        fig2.savefig('Preprossed_Leads_1-12_figure.png')

        fig3, ax3 = plt.subplots()
        grayscale = color.rgb2gray(Leads[-1])
        blurred = gaussian(grayscale, sigma=1)
        thresh = threshold_otsu(blurred)
        binary = blurred < thresh

        ax3.imshow(binary, cmap='gray')
        ax3.axis('off')
        fig3.savefig('Preprossed_Leads_13_figure.png')

    def SignalExtraction_Scaling(self, Leads):

        fig4, ax4 = plt.subplots(4, 3)

        x_counter = 0
        y_counter = 0

        for x, y in enumerate(Leads[:-1]):

            grayscale = color.rgb2gray(y)
            blurred = gaussian(grayscale, sigma=0.7)
            thresh = threshold_otsu(blurred)
            binary = resize(blurred < thresh, (300, 450))

            contours = measure.find_contours(binary, 0.8)
            largest = max(contours, key=lambda arr: arr.shape[0])
            test = resize(largest, (255, 2))

            ax4[x_counter][y_counter].invert_yaxis()
            ax4[x_counter][y_counter].plot(test[:, 1], test[:, 0])

            if (x + 1) % 3 == 0:
                x_counter += 1
                y_counter = 0
            else:
                y_counter += 1

            scaler = MinMaxScaler()
            scaled = scaler.fit_transform(test)

            df = pd.DataFrame(scaled[:, 0]).T
            df.to_csv(f'Scaled_1DLead_{x+1}.csv', index=False)

        fig4.savefig('Contour_Leads_1-12_figure.png')

    def CombineConvert1Dsignal(self):

        base_dir = os.path.dirname(__file__)

        test_final = pd.read_csv(os.path.join(base_dir, 'Scaled_1DLead_1.csv'))

        for file in natsorted(os.listdir(base_dir)):
            if file.startswith('Scaled_1DLead_') and file.endswith('.csv') and file != 'Scaled_1DLead_1.csv':
                df = pd.read_csv(os.path.join(base_dir, file))
                test_final = pd.concat([test_final, df], axis=1, ignore_index=True)

        return test_final

    def DimensionalReduciton(self, test_final):

        base_dir = os.path.dirname(__file__)

        pca_model = joblib.load(os.path.join(base_dir, 'PCA_ECG (1).pkl'))
        result = pca_model.transform(test_final)

        return pd.DataFrame(result)

    def ModelLoad_predict(self, final_df):

        base_dir = os.path.dirname(__file__)

        model = joblib.load(os.path.join(base_dir, 'Heart_Disease_Prediction_using_ECG (4).pkl'))
        result = model.predict(final_df)

        if result[0] == 1:
            return "You ECG corresponds to Myocardial Infarction"
        elif result[0] == 0:
            return "You ECG corresponds to Abnormal Heartbeat"
        elif result[0] == 2:
            return "Your ECG is Normal"
        else:
            return "You ECG corresponds to History of Myocardial Infarction"