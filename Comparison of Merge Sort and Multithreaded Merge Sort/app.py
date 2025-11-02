from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

# --- Merge Sort ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left if left else right)
    return result

# --- Threaded Merge Sort ---
def threaded_merge_sort(arr, result_container):
    result_container.append(merge_sort(arr))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    arr = data.get('array', [])
    sort_type = data.get('type', 'normal')

    if not arr:
        return jsonify({"error": "Array is empty"}), 400

    if sort_type == 'normal':
        start = time.time()
        merge_sort(arr.copy())
        end = time.time()
        return jsonify({"type": "Merge Sort", "time": round((end - start) * 1000, 2)})

    elif sort_type == 'threaded':
        start = time.time()
        mid = len(arr) // 2
        left, right = arr[:mid], arr[mid:]
        result_left, result_right = [], []

        t1 = threading.Thread(target=threaded_merge_sort, args=(left, result_left))
        t2 = threading.Thread(target=threaded_merge_sort, args=(right, result_right))
        t1.start(); t2.start()
        t1.join(); t2.join()

        merge(result_left[0], result_right[0])
        end = time.time()
        return jsonify({"type": "Multithreaded Merge Sort", "time": round((end - start) * 1000, 2)})

if __name__ == '__main__':
    app.run(debug=True)
