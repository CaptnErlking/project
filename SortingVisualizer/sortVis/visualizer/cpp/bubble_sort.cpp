#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <string>

using namespace std;

vector<vector<int>> steps;

void recordStep(int arr[], int n) {
    vector<int> temp(arr, arr + n);
    steps.push_back(temp);
}

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
            recordStep(arr, n);
        }
    }
}

void exportStepsToFile(const string& filename) {
    ofstream outFile(filename);

    // Check if the file was opened correctly
    if (!outFile.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return;
    }

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
    if (argc < 3) {
        cerr << "Please provide the array size and output filename as arguments!" << endl;
        return 1;
    }

    int size = stoi(argv[1]); // Get the array size from the command line argument

    srand(time(0));

    int arr[size];
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100;
    }

    steps.clear();
    bubbleSort(arr, size);
    exportStepsToFile(argv[2]);  // Save the output to the specified JSON file

    return 0;
}
