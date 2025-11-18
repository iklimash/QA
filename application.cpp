#include "application.h"

#include <iostream>
#include <limits>

using namespace std;

Application::Application() {}

inline void clear()
{
	cout << "\x1B[2J\x1B[H";
}

inline void clearInputStream() {
	cin.clear();
	cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

void Application::mainMenu()
{
	int choice;

	while (true)
	{
		cout << "1 - Dynamic array\n";
		cout << "2 - List\n";
		cout << "3 - Sort station\n";
		cout << "0 - Exit\n> ";
		cin >> choice;
		clearInputStream();
		switch (choice)
		{
		case 1:
			clear();
			appArray();
			clear();
			break;
		case 2:
			clear();
			appList();
			clear();
			break;
		case 3:
			clear();
			appStation();
			clear();
			break;
		case 0:
			return;
		default:
			break;
		}
	}
}

void Application::workMenu()
{
	cout << "1 - Create and fill\n"; //done
	cout << "2 - Print elements\n"; //done
	cout << "3 - Insert element\n"; //done
	cout << "4 - Delete element by index\n"; // done
	cout << "5 - Get an element by index\n"; //done
	cout << "6 - Swap elements\n";
	cout << "0 - Exit\n" << "> "; //done

}

int Application::appArray()
{
	int choice, value;
	int index1, index2;
	int* element;
	short index;
	auto* array = new Array<int>();
	while (true)
	{
		workMenu();
		cin >> choice;
		clearInputStream();
		switch (choice)
		{
		case 1:
			cout << "Input numbers please: ";
			delete array;
			array = new Array<int>();
			while (cin >> value) {
				array->pushBack(value);
				if (cin.peek() == '\n') {
					break;
				}
			}
			clearInputStream();
			clear();
			cout << "Your current array: ";
			array->print();
			cout << endl;
			break;
		case 2:
			clear();
			cout << "Array contents: ";
			array->print();
			cout << endl;
			break;
		case 3:
			cout << "Input index and value please: ";
			cin >> index; cin >> value;
			array->insertElement(index, value);
			clear();
			cout << "Array contents: ";
			array->print();
			cout << endl;
			break;
		case 4:
			cout << "Input index please: ";
			cin >> index;
			array->deleteElement(index);
			clear();
			cout << "Array contents: ";
			array->print();
			cout << endl;
			break;
		case 5:
			cout << "Input index please: ";
			cin >> index;
			clearInputStream();
			element = array->getElement(index);
			clear();
			if (element != nullptr) {
				cout << "Element at index " << index << ": " << *element << endl;
			}
			else {
				cout << "Invalid index!" << endl;
			}
			break;
		case 6:
			cout << "Input index1 and index2 please: ";
			cin >> index1; cin >> index2;
			array->swap(index1, index2);
			clear();
			cout << "Array contents: ";
			array->print();
			cout << endl;
			break;
		case 0:
			delete array;
			return 0;

		default:
			break;
		}
	}

}

int Application::appList()
{
	short index, index1,index2;
	int choice, value;
	auto* list = new List<int>();
	while (true)
	{
		workMenu();
		cin >> choice;
		clearInputStream();
		switch (choice)
		{
		case 1:
			cout << "Input numbers please: ";
			delete list;
			list = new List<int>();
			while (cin >> value) {
				list->pushBack(value);
				if (cin.peek() == '\n') {
					break;
				}
			}
			clearInputStream();
			clear();
			cout << "Your current list: ";
			list->print();
			cout << endl;
			break;
		case 2:
			clear();
			cout << "List contents: ";
			list->print();
			cout << endl;
			break;
		case 3:
			cout << "Input index and value please: ";
			cin >> index; cin >> value;
			if (cin.fail())
			{
				clearInputStream();
				cout << "\n�������� ����";
				break;
			}
			list->insert(index, value);
			clear();
			cout << "List contents: ";
			list->print();
			cout << endl;
			break;
		case 4:
			cout << "Input index please: ";
			cin >> index;
			if (cin.fail())
			{
				clearInputStream();
				cout << "\n�������� ����";
				break;
			}
			list->deleteKnot(index);
			clear();
			cout << "List contents: ";
			list->print();
			cout << endl;
			break;
		case 5:
			cout << "Input index please: ";
			cin >> index;
			if (cin.fail())
			{
				clearInputStream();
				cout << "\n�������� ����";
				break;
			}
			clearInputStream();
			clear();
			if (list->getKnot(index) != nullptr) {
				cout << "Element at index " << index << ": " << list->getKnot(index)->values << endl << endl;
			}
			else {
				cout << "Invalid index!" << endl << endl;
			}
			break;
		case 6:
			cout << "Input index1 and index2 please: ";
			cin >> index1; cin >> index2;
			if (cin.fail())
			{
				clearInputStream();
				cout << "\n�������� ����";
				break;
			}
			list->swap(index1, index2);
			clear();
			cout << "Array contents: ";
			list->print();
			cout << endl;
			break;

		case 0:
			delete list;
			return 0;
		default:
			break;
		}
	}

}

int Application::appStation()
{
	SortStation station;
	string input;
	int choise;
	bool flag = false;

	while (true)
	{
		cout << "1 - Convert the expression to reverse Polish notation\n";
		cout << "0 - Exit\n" << "> ";
		cin >> choise;
		switch (choise) {
		case 1:
			cout << "Input expression: ";
			clearInputStream();
			input = station.getString();
			input = station.ReversPolishnotation(input, flag);
			if (flag == true || input.empty())
			{
				cout << "Error expression";
				break;
			}
			if (station.calculateValue(input))
			{
				cout << "Expression in reverse Polish notation: " << input;
			}
			else
			{
				cout << "Error expression";
			}
			break;
		case 0:
			return 0;
		default:
			cout << "Error expression";
			break;
		}
		cout << "\n";
	}

}