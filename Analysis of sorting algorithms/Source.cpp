#include<iostream>
#include<vector>
#include<algorithm>
#include<fstream>
#include<random>
#include<chrono>
#include<iomanip>

using namespace std;
using namespace chrono;

ifstream inFile;
ofstream outFile;

random_device rd;
mt19937_64 mt(rd());
uniform_int_distribution<>dist(0, 1000);

vector<unsigned long long>a;

void fill_File(int size) {
	outFile.open("numbers.txt", ios_base::trunc);

	int i = 0;
	while (i != size) {
		outFile << dist(mt) << "\n";
		i++;
	}
	outFile.close();
}

void reset() {
	//clear the file and return pointer to the begining of file
	inFile.clear();
	inFile.seekg(0, ios_base::beg);
}

void BubbleSort(vector<unsigned long long> &vec) {
	for (unsigned long long i = 0; i < vec.size(); i++) {
		for (unsigned long long j = i + 1; j < vec.size(); j++) {
			if (vec[static_cast<size_t>(j)] > vec[static_cast<size_t>(i)])
				swap(vec[static_cast<size_t>(j)], vec[static_cast<size_t>(i)]);
		}
	}
}

void InsertionSort(vector<unsigned long long> &vec) {
	unsigned long long key;
	
	for (unsigned long long i = 1; i < vec.size(); i++) {
		key = vec[static_cast<size_t>(i)];
		unsigned long long j = i;

		while (static_cast<size_t>(j) > 0 && vec[static_cast<size_t>(j-1)] > key) {
			vec[static_cast<size_t>(j)] = vec[static_cast<size_t>(j-1)];
			j--;
		}
		vec[static_cast<size_t>(j)] = key;
	}
}

void Merge(vector<unsigned long long>& vec, 
	unsigned long long low, unsigned long long mid, unsigned long long high) {
	//split from the middle
	vector<unsigned long long>leftVec(static_cast<size_t>(mid - low + 1));
	vector<unsigned long long>rightVec(static_cast<size_t>(high - mid));

	//fill in the left list
	for (size_t i = 0; i < leftVec.size(); i++)
		leftVec[i] = vec[(size_t)(low + i)];

	//fill in the right list
	for (size_t i = 0; i < rightVec.size(); i++)
		rightVec[i] = vec[(size_t)(mid + 1 + i)];

	// initial indexes of first and second subarrays
	unsigned long long leftIndex = 0, rightIndex = 0;

	// the index we will start at when adding the subarrays back into the main array
	unsigned long long currentIndex = low;

	// compare each index of the subarrays adding the lowest value to the currentIndex
	while (leftIndex < leftVec.size() && rightIndex < rightVec.size()) {
		if (leftVec[(size_t)(leftIndex)] <= rightVec[(size_t)(rightIndex)]) {
			vec[(size_t)(currentIndex)] = leftVec[(size_t)(leftIndex)];
			leftIndex++;
		}
		else {
			vec[(size_t)(currentIndex)] = rightVec[(size_t)(rightIndex)];
			rightIndex++;
		}
		currentIndex++;
	}

	// copy remaining elements of leftArray[] if any
	while (leftIndex < leftVec.size()) {
		vec[(size_t)(currentIndex)] = leftVec[(size_t)(leftIndex)];
		currentIndex++;
		leftIndex++;
	}

	// copy remaining elements of rightArray[] if any
	while (rightIndex < rightVec.size()) {
		vec[(size_t)(currentIndex)] = rightVec[(size_t)(rightIndex)];
		currentIndex++;
		rightIndex++;
	}
}

void MergeSort(vector<unsigned long long>& vec, 
	unsigned long long low, unsigned long long high) {

	//base case
	if (low < high) {
		unsigned long long mid = (low + high) / 2;

		//sort left list
		MergeSort(vec, low, mid);

		//sort right list
		MergeSort(vec, mid + 1, high);

		//merge the lists
		Merge(vec, low, mid, high);
	}
}

int main() {
	
	inFile.open("numbers.txt");
	outFile.open("numbers.txt");

	if (!inFile || !outFile) {
		cerr << "Error opening file!";
		return 0;
	}

	unsigned long long x;

	cout << "\t\t\t\tRuntime Analysis\n\nFile Size\tBubble Sort\tInsertion Sort\tMerge Sort\n";

	double sumBubbleTime = 0;
	double sumInsertionTime = 0;
	double sumMergeTime = 0;

	for (int i = 500; i < 10500; i += 500) {
		//fill the file with random numbers
		fill_File(i);

		//Clear the vector to avoid errors. Then, copy the file contents into the vector. 
		a.clear();
		a.shrink_to_fit();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		auto t1 = high_resolution_clock::now();
		BubbleSort(a);
		auto t2 = high_resolution_clock::now();

		duration<double, milli>BubbleSortTime = t2 - t1;
		sumBubbleTime += BubbleSortTime.count();

		reset();

		//Clear the vector to avoid errors. Then, copy the file contents into the vector. 
		a.clear();
		a.shrink_to_fit();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		auto t3 = high_resolution_clock::now();
		InsertionSort(a);
		auto t4 = high_resolution_clock::now();

		duration<double, milli>InsertionSortTime = t4 - t3;
		sumInsertionTime += InsertionSortTime.count();

		reset();

		//Clear the vector to avoid errors. Then, copy the file contents into the vector. 
		a.clear();
		a.shrink_to_fit();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		auto t5 = high_resolution_clock::now();
		MergeSort(a, 0, a.size() - 1);
		auto t6 = high_resolution_clock::now();

		duration<double, milli>MergeSortTime = t6 - t5;
		sumMergeTime += MergeSortTime.count();

		reset();

		//Clear the vector to avoid errors. Then, copy the file contents into the vector. 
		a.clear();
		a.shrink_to_fit();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		cout << setw(5) << i << "\t\t" << sumBubbleTime << "\t\t"
			<< setw(5) << sumInsertionTime << "\t\t"
			<< setw(5) << sumMergeTime << endl;
	}

	inFile.close();
	outFile.close();
	return 0;
}