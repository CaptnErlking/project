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

void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        swap(arr[i], arr[minIdx]);
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
    selectionSort(arr, size);
    exportStepsToFile(argv[2]);  // Save the output to the specified JSON file

    return 0;
}
