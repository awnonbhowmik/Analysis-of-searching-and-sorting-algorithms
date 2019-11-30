#include<iostream>
#include<fstream>
#include<vector>
#include<algorithm>
#include<chrono>
#include<ctime>
#include<random>
#include<iomanip>
#include<tuple>

using namespace std;
using namespace chrono;

random_device rd;
mt19937_64 mt(rd());
uniform_int_distribution<> dist(0, (int)pow(10, 9));

long long int ls_index;
long long int bs_index;

unsigned long long count_binary = 0;

ifstream inFile;
ofstream outFile;

void fill_File(int size) {
	outFile.open("numbers.txt", ios_base::trunc);

	int i = 0;
	while (i != size) {
		outFile << dist(mt) << "\n";
		i++;
	}
	outFile.close();
}

tuple<long long, unsigned long long>
LinearSearch(vector<unsigned long long>vec, unsigned long long x) {
	long long ls_index = -1;
	unsigned long long count_linear = 0;
	for (unsigned long long i = 0; i < vec.size(); i++) {
		count_linear++;
		if (vec[static_cast<size_t>(i)] == x) {
			ls_index = i;
			break;
		}
	}
	return { ls_index,count_linear };
}

tuple<long long, unsigned long long>
BinarySearch(vector<unsigned long long>vec,
	unsigned long long low, unsigned long long high, unsigned long long x) {

	while (low < high)
	{
		unsigned long long mid = (low + high) / 2;
		count_binary++;
		if (low <= mid || mid >= high) {
			bs_index = -1;
			return { bs_index,count_binary };
		}
		else if (x > vec[static_cast<size_t>(mid)])
			return BinarySearch(vec, mid + 1, high, x);
		else if (x < vec[static_cast<size_t>(mid)])
			return BinarySearch(vec, low, mid - 1, x);
		else {
			bs_index = mid;
			return { bs_index,count_binary };
		}
	}

	return { -1,count_binary };
}

int main(int argc, char** argv) {
	vector<unsigned long long>a;

	inFile.open("numbers.txt");
	outFile.open("numbers.txt");

	if (!inFile || !outFile) {
		cerr << "Error opening file";
		return 0;
	}

	unsigned long long x, y;

	cout << "Sequential Search\n\nFile Size\tNumber\tIndex\tTime\tNumber of steps\n";

	double SumLinearSearch = 0;
	for (int i = 1; i <= 22; i++) {

		fill_File((int)pow(2, i));

		a.clear();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		//Clear the file and return pointer to beginning of file
		inFile.clear();
		inFile.seekg(0, ios_base::beg);

		y = dist(mt);

		long long ls_index;
		unsigned long long ls_count;

		auto t1 = high_resolution_clock::now();
		tie(ls_index, ls_count) = LinearSearch(a, y);
		auto t2 = high_resolution_clock::now();

		duration<double, milli> diff = t2 - t1;
		SumLinearSearch += diff.count();

		cout << setw(7) << (int)pow(2, i) << setw(15) << y << "\t"
			<< setw(3) << ls_index << setw(10) << SumLinearSearch << "\t" << setw(8) << ls_count << "\n";
	}

	cout << "\n\nBinary Search\n\nFile Size\tNumber\tIndex\tTime\tNumber of Steps\n";

	double SumBinarySearch = 0;
	for (int i = 1; i <= 22; i++) {

		fill_File((int)pow(2, i));

		a.clear();
		while (!inFile.eof()) {
			inFile >> x;
			a.push_back(x);
		}

		unsigned long long low = 0;
		unsigned long long high = a.size() - 1;

		/*Notice that here in Binary Search, the function is written so
		that the program always knows which index to search from, this
		is why we don't need to rewind the file pointer to look for the
		starting and ending point.*/

		//Binary search requires the list to be sorted
		sort(a.begin(), a.end());

		y = dist(mt);

		long long bs_index;
		unsigned long long bs_count;

		auto t3 = high_resolution_clock::now();
		tie(bs_index, bs_count) = BinarySearch(a, low, high, y);
		auto t4 = high_resolution_clock::now();

		duration<double, milli>diff = t4 - t3;
		SumBinarySearch += diff.count();

		cout << setw(7) << (int)pow(2, i) << setw(15) << y << "\t"
			<< setw(3) << bs_index << setw(12) << SumBinarySearch << "\t" << setw(5) << bs_count << "\n";
	}

	inFile.close();
	outFile.close();
	return 0;
}