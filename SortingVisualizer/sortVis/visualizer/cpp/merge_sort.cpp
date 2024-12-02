#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

vector<vector<int>> steps;

void recordStep(int arr[], int n) {
    vector<int> temp(arr, arr + n);
    steps.push_back(temp);
}

void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> leftArr(n1), rightArr(n2);

    for (int i = 0; i < n1; i++) leftArr[i] = arr[left + i];
    for (int i = 0; i < n2; i++) rightArr[i] = arr[mid + 1 + i];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (leftArr[i] <= rightArr[j]) {
            arr[k++] = leftArr[i++];
        } else {
            arr[k++] = rightArr[j++];
        }
        recordStep(arr, right + 1);
    }

    while (i < n1) arr[k++] = leftArr[i++];
    while (j < n2) arr[k++] = rightArr[j++];

    recordStep(arr, right + 1);
}

void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

void exportStepsToFile(const string& filename) {
    string filePath = "../static/json/sorting/" + filename;
    ofstream outFile(filePath);
    outFile << "[";
    for (size_t i = 0; i < steps.size(); i++) {
        outFile << "[";
        for (size_t j = 0; j < steps[i].size(); j++) {
            outFile << steps[i][j];
            if (j != steps[i].size() - 1) outFile << ",";
        }
        outFile << "]";
        if (i != steps.size() - 1) outFile << ",";
    }
    outFile << "]";
    outFile.close();
}

int main(int argc, char* argv[]) {
    int size = stoi(argv[1]); // Get the array size from the command line argument

    srand(time(0));

    int arr[size];
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100;
    }

    steps.clear();
    mergeSort(arr, 0, size - 1);
    exportStepsToFile(argv[2]);  // Save the output to the specified JSON file

    return 0;
}
