import requests
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def load_test(url, duration_seconds=30):
    response_times = []
    start_time = time.time()
    end_time = start_time + duration_seconds
    
    print(f"Starting load test for {duration_seconds} seconds...")
    print(f"Testing URL: {url}")
    print("-" * 60)
    
    while time.time() < end_time:
        try:
            start_request = time.time()
            response = requests.get(url, timeout=10)
            end_request = time.time()
            
            response_time = (end_request - start_request) * 1000  # Convert to milliseconds
            response_times.append(response_time)
            
            if response.status_code == 200:
                print(f"Request {len(response_times)}: {response_time:.2f}ms - SUCCESS")
            else:
                print(f"Request {len(response_times)}: Failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            
    return response_times

EC2_URL = "http://13.220.91.38:8080/albums"

# Run the test
print("=" * 60)
print("LOAD TESTING YOUR EC2 API")
print("=" * 60)
response_times = load_test(EC2_URL, duration_seconds=30)

# Calculate statistics
total_requests = len(response_times)
avg_response = np.mean(response_times)
median_response = np.median(response_times)
percentile_95 = np.percentile(response_times, 95)
percentile_99 = np.percentile(response_times, 99)
max_response = max(response_times)
min_response = min(response_times)
std_dev = np.std(response_times)

# Print statistics
print("\n" + "=" * 60)
print("PERFORMANCE STATISTICS")
print("=" * 60)
print(f"Total requests completed: {total_requests}")
print(f"Average response time:    {avg_response:.2f}ms")
print(f"Median response time:     {median_response:.2f}ms")
print(f"Standard deviation:       {std_dev:.2f}ms")
print(f"Min response time:        {min_response:.2f}ms")
print(f"Max response time:        {max_response:.2f}ms")
print(f"95th percentile:          {percentile_95:.2f}ms")
print(f"99th percentile:          {percentile_99:.2f}ms")
print("=" * 60)

# Calculate percentage of "slow" requests (over 500ms)
slow_threshold = 500
slow_requests = sum(1 for rt in response_times if rt > slow_threshold)
slow_percentage = (slow_requests / total_requests) * 100
print(f"\nRequests over {slow_threshold}ms: {slow_requests} ({slow_percentage:.1f}%)")

# Calculate gap between median and 95th percentile
gap = percentile_95 - median_response
print(f"Gap between median and 95th percentile: {gap:.2f}ms")

# Plot the results
plt.figure(figsize=(14, 7))

# Histogram
plt.subplot(3, 1, 1)
plt.hist(response_times, bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(median_response, color='red', linestyle='--', linewidth=2, label=f'Median: {median_response:.2f}ms')
plt.axvline(percentile_95, color='orange', linestyle='--', linewidth=2, label=f'95th %ile: {percentile_95:.2f}ms')
plt.xlabel('Response Time (ms)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Response Times (Histogram)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Scatter plot over time
plt.subplot(3, 1, 2)
plt.scatter(range(len(response_times)), response_times, alpha=0.6, color='green')
plt.axhline(median_response, color='red', linestyle='--', linewidth=2, label=f'Median: {median_response:.2f}ms')
plt.axhline(percentile_95, color='orange', linestyle='--', linewidth=2, label=f'95th %ile: {percentile_95:.2f}ms')
plt.xlabel('Request Number', fontsize=12)
plt.ylabel('Response Time (ms)', fontsize=12)
plt.title('Response Times Over Time', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('load_test_results.png', dpi=300, bbox_inches='tight')
print(f"\nGraph saved as 'load_test_results.png'")
plt.show()

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)