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

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
            recordStep(arr, n);
        }
        arr[j + 1] = key;
        recordStep(arr, n);
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
    insertionSort(arr, size);
    exportStepsToFile(argv[2]);  // Save the output to the specified JSON file

    return 0;
}
