#include "RC4.hh"

using namespace std;
int main()
{
	ifstream input_file("in.txt", ios::binary);
	if (!input_file)
	{
		cerr << "Can't open in.txt" << endl;
		return 1;
	}

	vector<unsigned char> input_data((istreambuf_iterator<char>(input_file)), istreambuf_iterator<char>());
	input_file.close();

	string key;
	cout << "Input key:" << endl;
	cin >> key;
	RC4 rc4(key);

	// 对明文进行加密
	vector<unsigned char> encrypted_data = rc4.encrypt_decrypt(input_data);

	// 将密文写入文件
	ofstream output_file("out.txt", ios::binary);
	if (!output_file)
	{
		cerr << "Can't open out.txt" << endl;
		return 1;
	}

	output_file.write(reinterpret_cast<char *>(encrypted_data.data()), encrypted_data.size());
	output_file.close();

	cout << "Success!" << endl;

	return 0;
}
