import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Sample eye distances data
eye_distances = [1, 4.1, 0.1, 2.3]

def analyze_eye_distances(distances):
    """
    Analyze caterpillar eye distances using linear regression and mean squared error.
    
    Args:
        distances (list): List of eye distances measurements
    
    Returns:
        dict: Analysis results including trend and MSE
    """
    # Convert to numpy array and reshape for sklearn
    X = np.arange(len(distances)).reshape(-1, 1)
    y = np.array(distances)
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate mean squared error
    mse = mean_squared_error(y, y_pred)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual distances')
    plt.plot(X, y_pred, color='red', label='Linear trend')
    plt.xlabel('Measurement Index')
    plt.ylabel('Eye Distance')
    plt.title('Caterpillar Eye Distance Analysis')
    plt.legend()
    plt.savefig('eye_distance_analysis.png')
    plt.close()
    
    return {
        'slope': model.coef_[0],
        'intercept': model.intercept_,
        'mse': mse,
        'trend': 'increasing' if model.coef_[0] > 0 else 'decreasing'
    }

if __name__ == '__main__':
    results = analyze_eye_distances(eye_distances)
    print(f"Analysis Results:")
    print(f"Trend: {results['trend']}")
    print(f"Mean Squared Error: {results['mse']:.4f}")
    print(f"Slope: {results['slope']:.4f}")
    print(f"Intercept: {results['intercept']:.4f}")