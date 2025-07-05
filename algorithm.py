import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class DiscretizationAlgorithms:
    """
    Class chứa các thuật toán discretization khác nhau
    """
    
    @staticmethod
    def equal_width_binning(data, n_bins=10):
        """
        Equal Width Binning (Uniform Binning)
        Chia dữ liệu thành các bin có độ rộng bằng nhau
        """
        min_val = data.min()
        max_val = data.max()
        bin_width = (max_val - min_val) / n_bins
        
        bins = []
        bin_labels = []
        
        for i in range(n_bins):
            start = min_val + i * bin_width
            end = min_val + (i + 1) * bin_width
            bins.append((start, end))
            bin_labels.append(f"Bin_{i+1}")
        
        # Phân loại dữ liệu vào các bin
        discretized = []
        for value in data:
            for i, (start, end) in enumerate(bins):
                if start <= value <= end:
                    discretized.append(bin_labels[i])
                    break
        
        return discretized, bins, bin_labels
    
    @staticmethod
    def equal_frequency_binning(data, n_bins=10):
        """
        Equal Frequency Binning (Quantile Binning)
        Chia dữ liệu thành các bin có số lượng phần tử bằng nhau
        """
        sorted_data = np.sort(data)
        n_samples = len(data)
        samples_per_bin = n_samples // n_bins
        
        bin_labels = [f"Bin_{i+1}" for i in range(n_bins)]
        discretized = []
        
        for value in data:
            # Tìm vị trí của value trong sorted_data
            position = np.searchsorted(sorted_data, value)
            bin_index = min(position // samples_per_bin, n_bins - 1)
            discretized.append(bin_labels[bin_index])
        
        return discretized, bin_labels
    
    @staticmethod
    def kmeans_binning(data, n_bins=5):
        """
        K-Means Binning
        Sử dụng K-Means clustering để tạo các bin
        """
        # Reshape data cho KMeans
        X = data.values.reshape(-1, 1)
        
        # Áp dụng KMeans
        kmeans = KMeans(n_clusters=n_bins, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)
        
        # Tạo bin labels
        bin_labels = [f"Bin_{i+1}" for i in range(n_bins)]
        discretized = [bin_labels[cluster] for cluster in clusters]
        
        return discretized, bin_labels
    
    @staticmethod
    def jenks_natural_breaks(data, n_bins=5):
        """
        Jenks Natural Breaks
        Tìm các điểm break tự nhiên trong dữ liệu
        """
        # Sử dụng KBinsDiscretizer với strategy='quantile' để mô phỏng Jenks
        # (vì sklearn không có Jenks trực tiếp)
        discretizer = KBinsDiscretizer(n_bins=n_bins, strategy='quantile', encode='ordinal')
        discretized_numeric = discretizer.fit_transform(data.values.reshape(-1, 1)).flatten()
        
        bin_labels = [f"Bin_{i+1}" for i in range(n_bins)]
        discretized = [bin_labels[int(val)] for val in discretized_numeric]
        
        return discretized, bin_labels
    
    @staticmethod
    def standard_deviation_binning(data, n_std=1):
        """
        Standard Deviation Binning
        Chia dữ liệu dựa trên độ lệch chuẩn
        """
        mean_val = data.mean()
        std_val = data.std()
        
        # Tạo các ngưỡng dựa trên độ lệch chuẩn
        thresholds = []
        for i in range(-n_std, n_std + 1):
            thresholds.append(mean_val + i * std_val)
        
        bin_labels = [f"Bin_{i+1}" for i in range(len(thresholds) - 1)]
        discretized = []
        
        for value in data:
            for i in range(len(thresholds) - 1):
                if thresholds[i] <= value < thresholds[i + 1]:
                    discretized.append(bin_labels[i])
                    break
            else:
                # Nếu value >= threshold cuối cùng
                discretized.append(bin_labels[-1])
        
        return discretized, bin_labels
    
    @staticmethod
    def custom_binning(data, custom_bins):
        """
        Custom Binning
        Cho phép người dùng định nghĩa các bin tùy chỉnh
        """
        bin_labels = [f"Bin_{i+1}" for i in range(len(custom_bins) - 1)]
        discretized = []
        
        for value in data:
            for i in range(len(custom_bins) - 1):
                if custom_bins[i] <= value < custom_bins[i + 1]:
                    discretized.append(bin_labels[i])
                    break
            else:
                # Nếu value >= threshold cuối cùng
                discretized.append(bin_labels[-1])
        
        return discretized, bin_labels

def get_algorithm_info():
    """
    Trả về thông tin về các thuật toán có sẵn
    """
    algorithms = {
        "Equal Width Binning": {
            "description": "Chia dữ liệu thành các bin có độ rộng bằng nhau",
            "parameters": {
                "n_bins": {"type": "int", "default": 10, "min": 2, "max": 50, "description": "Số lượng bin"}
            },
        
        },
        "Equal Frequency Binning": {
            "description": "Chia dữ liệu thành các bin có số lượng phần tử bằng nhau",
            "parameters": {
                "n_bins": {"type": "int", "default": 10, "min": 2, "max": 50, "description": "Số lượng bin"}
            },
            
        },
        "KMeans Binning": {
            "description": "Sử dụng K-Means clustering để tạo các bin",
            "parameters": {
                "n_bins": {"type": "int", "default": 5, "min": 2, "max": 20, "description": "Số lượng cluster/bin"}
            },
            
        },
        "Jenks Natural Breaks": {
            "description": "Tìm các điểm break tự nhiên trong dữ liệu",
            "parameters": {
                "n_bins": {"type": "int", "default": 5, "min": 2, "max": 20, "description": "Số lượng break points"}
            },
            
        },
        "Standard Deviation Binning": {
            "description": "Chia dữ liệu dựa trên độ lệch chuẩn",
            "parameters": {
                "n_std": {"type": "int", "default": 1, "min": 1, "max": 3, "description": "Số độ lệch chuẩn"}
            },
            
        }
    }
    
    return algorithms 