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

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
            recordStep(arr, high + 1);
        }
    }
    swap(arr[i + 1], arr[high]);
    recordStep(arr, high + 1);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
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
    quickSort(arr, 0, size - 1);
    exportStepsToFile(argv[2]);  // Save the output to the specified JSON file

    return 0;
}
