"""
SSIM-based Visual Testing Engine for TestAutothon2824 Framework
Minimal implementation adapted from DISNEY_AEM framework
"""
import os
import time
from typing import Dict, Optional, Tuple
from pathlib import Path

import cv2
import numpy as np
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SSIMVisualConfig:
    """Configuration for SSIM-based visual testing."""
    
    # SSIM Thresholds
    SSIM_THRESHOLDS = {
        'strict': 0.95,      # For critical UI elements
        'moderate': 0.85,    # For content areas with some dynamic elements
        'relaxed': 0.75      # For areas with ads, timestamps, etc.
    }
    
    # Directories
    SSIM_BASELINE_DIR = 'Outputs\\ssim_baselines'
    SSIM_DIFF_DIR = 'Outputs\\ssim_diffs'
    SSIM_PASS_DIR = 'Outputs\\ssim_pass'


class SSIMVisualEngine:
    """SSIM-based visual testing engine for dynamic content handling."""
    
    def __init__(self):
        """Initialize SSIM visual engine."""
        self.config = SSIMVisualConfig()
        self.baseline_dir = Path(self.config.SSIM_BASELINE_DIR)
        self.diff_dir = Path(self.config.SSIM_DIFF_DIR)
        self.pass_dir = Path(self.config.SSIM_PASS_DIR)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories."""
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)
        self.pass_dir.mkdir(parents=True, exist_ok=True)
    
    def capture_screenshot(self, driver: WebDriver, name: str, 
                          element_selector: Optional[str] = None) -> str:
        """Capture screenshot with stabilization for dynamic content."""
        # Wait for page to stabilize
        time.sleep(2)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_ssim_{timestamp}.png"
        temp_dir = Path("Outputs\\temp_screenshots")
        temp_dir.mkdir(exist_ok=True)
        filepath = temp_dir / filename
        
        if element_selector:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )
            element.screenshot(str(filepath))
        else:
            driver.save_screenshot(str(filepath))
        
        return str(filepath)
    
    def calculate_ssim(self, baseline_path: str, current_path: str, 
                      threshold: float = 0.85) -> Dict:
        """Calculate SSIM between two images using OpenCV-based implementation."""
        if not os.path.exists(baseline_path):
            return {
                "match": False,
                "error": "Baseline image not found",
                "ssim_score": 0.0
            }
        
        # Load images in grayscale for SSIM calculation
        baseline = cv2.imread(baseline_path, cv2.IMREAD_GRAYSCALE)
        current = cv2.imread(current_path, cv2.IMREAD_GRAYSCALE)
        
        if baseline is None or current is None:
            return {
                "match": False,
                "error": "Failed to load images",
                "ssim_score": 0.0
            }
        
        # Resize images to same dimensions if needed
        if baseline.shape != current.shape:
            current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))
        
        # Calculate SSIM using OpenCV-based method
        ssim_score, ssim_diff = self._calculate_opencv_ssim(baseline, current)
        
        # Determine match based on threshold
        match = ssim_score >= threshold
        
        return {
            "match": match,
            "ssim_score": ssim_score,
            "threshold": threshold,
            "ssim_diff": ssim_diff,
            "baseline_shape": baseline.shape,
            "current_shape": current.shape
        }
    
    def _calculate_opencv_ssim(self, img1: np.ndarray, img2: np.ndarray) -> Tuple[float, np.ndarray]:
        """Calculate SSIM using OpenCV-based implementation."""
        # Convert to float
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        # Constants for SSIM calculation
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2
        
        # Calculate means
        mu1 = cv2.GaussianBlur(img1, (11, 11), 1.5)
        mu2 = cv2.GaussianBlur(img2, (11, 11), 1.5)
        
        mu1_sq = mu1 * mu1
        mu2_sq = mu2 * mu2
        mu1_mu2 = mu1 * mu2
        
        # Calculate variances and covariance
        sigma1_sq = cv2.GaussianBlur(img1 * img1, (11, 11), 1.5) - mu1_sq
        sigma2_sq = cv2.GaussianBlur(img2 * img2, (11, 11), 1.5) - mu2_sq
        sigma12 = cv2.GaussianBlur(img1 * img2, (11, 11), 1.5) - mu1_mu2
        
        # Calculate SSIM
        numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
        denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
        
        ssim_map = numerator / denominator
        ssim_score = np.mean(ssim_map)
        
        return ssim_score, ssim_map
    
    def create_ssim_diff_visualization(self, baseline_path: str, current_path: str, 
                                     ssim_diff: np.ndarray, output_path: str, 
                                     ssim_score: float):
        """Create SSIM difference visualization."""
        baseline = cv2.imread(baseline_path)
        current = cv2.imread(current_path)
        
        if baseline is None or current is None:
            return
        
        if baseline.shape != current.shape:
            current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))
        
        # Convert SSIM diff to heatmap
        ssim_diff_normalized = ((1 - ssim_diff) * 255).astype(np.uint8)
        heatmap = cv2.applyColorMap(ssim_diff_normalized, cv2.COLORMAP_JET)
        
        # Create comparison layout
        height = max(baseline.shape[0], current.shape[0]) + 80
        width = baseline.shape[1] + current.shape[1] + heatmap.shape[1] + 300
        
        comparison = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Place images
        comparison[80:80+baseline.shape[0], :baseline.shape[1]] = baseline
        
        start_x = baseline.shape[1] + 100
        comparison[80:80+current.shape[0], start_x:start_x+current.shape[1]] = current
        
        heatmap_start_x = start_x + current.shape[1] + 100
        comparison[80:80+heatmap.shape[0], heatmap_start_x:heatmap_start_x+heatmap.shape[1]] = heatmap
        
        # Add labels and SSIM score
        cv2.putText(comparison, 'BASELINE', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(comparison, 'CURRENT', (start_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(comparison, 'SSIM DIFF', (heatmap_start_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(comparison, f'SSIM Score: {ssim_score:.3f}', (width//2 - 100, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imwrite(output_path, comparison)
    
    def create_ssim_pass_visualization(self, baseline_path: str, current_path: str, 
                                     output_path: str, ssim_score: float):
        """Create SSIM pass visualization."""
        baseline = cv2.imread(baseline_path)
        current = cv2.imread(current_path)
        
        if baseline is None or current is None:
            return
        
        if baseline.shape != current.shape:
            current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))
        
        # Create side-by-side comparison
        height = max(baseline.shape[0], current.shape[0]) + 80
        width = baseline.shape[1] + current.shape[1] + 200
        
        comparison = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Place images
        comparison[80:80+baseline.shape[0], :baseline.shape[1]] = baseline
        comparison[80:80+current.shape[0], baseline.shape[1]+100:baseline.shape[1]+100+current.shape[1]] = current
        
        # Add labels
        cv2.putText(comparison, 'BASELINE', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(comparison, 'CURRENT', (baseline.shape[1] + 110, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(comparison, f'SSIM PASSED: {ssim_score:.3f}', (width//2 - 120, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 0), 2)
        
        cv2.imwrite(output_path, comparison)
    
    def ssim_visual_assert(self, driver: WebDriver, test_name: str,
                          element_selector: Optional[str] = None,
                          threshold: float = 0.85,
                          browser: str = "chrome") -> Dict:
        """Perform SSIM-based visual assertion."""
        baseline_name = f"{test_name}_{browser}_ssim_baseline.png"
        baseline_path = self.baseline_dir / baseline_name
        
        # Capture current screenshot
        current_path = self.capture_screenshot(driver, f"{test_name}_{browser}_current", element_selector)
        
        # Calculate SSIM
        ssim_result = self.calculate_ssim(str(baseline_path), current_path, threshold)
        
        # Create visualization paths
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        
        if ssim_result.get("match", False):
            # Create pass visualization
            pass_name = f"{test_name}_{browser}_ssim_pass_{timestamp}.png"
            pass_path = self.pass_dir / pass_name
            self.create_ssim_pass_visualization(
                str(baseline_path), current_path, str(pass_path), ssim_result["ssim_score"]
            )
            visualization_path = str(pass_path)
            visualization_type = "pass"
        else:
            # Create diff visualization
            diff_name = f"{test_name}_{browser}_ssim_diff_{timestamp}.png"
            diff_path = self.diff_dir / diff_name
            if "ssim_diff" in ssim_result:
                self.create_ssim_diff_visualization(
                    str(baseline_path), current_path, ssim_result["ssim_diff"], 
                    str(diff_path), ssim_result["ssim_score"]
                )
            visualization_path = str(diff_path)
            visualization_type = "diff"
        
        # Update result with additional info
        ssim_result.update({
            "test_name": test_name,
            "browser": browser,
            "baseline_path": str(baseline_path),
            "current_path": current_path,
            "visualization_path": visualization_path,
            "visualization_type": visualization_type,
            "comparison_method": "SSIM"
        })
        
        return ssim_result
    
    def create_baseline(self, driver: WebDriver, test_name: str,
                       element_selector: Optional[str] = None,
                       browser: str = "chrome") -> str:
        """Create SSIM baseline screenshot."""
        baseline_name = f"{test_name}_{browser}_ssim_baseline.png"
        baseline_path = self.baseline_dir / baseline_name
        
        # Wait for page stability
        time.sleep(3)
        
        if element_selector:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )
            element.screenshot(str(baseline_path))
        else:
            driver.save_screenshot(str(baseline_path))
        
        return str(baseline_path)


class SSIMVisualCheckpoint:
    """SSIM-based visual checkpoint utility for multiple validations."""
    
    def __init__(self, driver: WebDriver, threshold: float = 0.85, browser: str = "chrome"):
        """Initialize SSIM visual checkpoint."""
        self.driver = driver
        self.ssim_engine = SSIMVisualEngine()
        self.threshold = threshold
        self.browser = browser
        self.checkpoints = []
    
    def capture(self, checkpoint_name: str, element_selector: Optional[str] = None,
               threshold: Optional[float] = None) -> Dict:
        """Capture SSIM visual checkpoint."""
        threshold = threshold or self.threshold
        
        # Check if baseline exists
        baseline_path = self.ssim_engine.baseline_dir / f"{checkpoint_name}_{self.browser}_ssim_baseline.png"
        
        if not baseline_path.exists():
            print(f"⚠️  SSIM Baseline missing for {checkpoint_name}. Creating baseline...")
            self.ssim_engine.create_baseline(self.driver, checkpoint_name, element_selector, self.browser)
            print(f"✅ SSIM Baseline created: {baseline_path}")
            
            result = {
                "match": True,
                "test_name": checkpoint_name,
                "baseline_created": True,
                "baseline_path": str(baseline_path),
                "comparison_method": "SSIM"
            }
            self.checkpoints.append(result)
            return result
        
        # Perform SSIM comparison
        result = self.ssim_engine.ssim_visual_assert(
            self.driver, checkpoint_name, element_selector, threshold, self.browser
        )
        
        self.checkpoints.append(result)
        return result
    
    def assert_all_passed(self):
        """Assert that all SSIM visual checkpoints passed."""
        failed_checkpoints = [cp for cp in self.checkpoints if not cp.get("match", False)]
        
        if failed_checkpoints:
            failed_names = [cp.get("test_name", "unknown") for cp in failed_checkpoints]
            raise AssertionError(f"SSIM Visual checkpoints failed: {failed_names}")
        
        # Log summary
        baseline_created = [cp for cp in self.checkpoints if cp.get("baseline_created", False)]
        comparisons_passed = [cp for cp in self.checkpoints if cp.get("match", False) and not cp.get("baseline_created", False)]
        
        print(f"📸 Created {len(baseline_created)} SSIM baselines")
        print(f"✅ {len(comparisons_passed)} SSIM visual comparisons passed")