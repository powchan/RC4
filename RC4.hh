#include <iostream>
#include <fstream>
#include <vector>
#include <string>


// RC4加解密算法实现
class RC4 {
public:
    RC4(const std::string& key) {
        // 初始化密钥
        key_schedule(key);
    }

    // RC4加密解密函数
    std::vector<unsigned char> encrypt_decrypt(const std::vector<unsigned char>& input) {
        std::vector<unsigned char> output(input.size());
        int i = 0, j = 0;

        // 生成伪随机密钥流并与输入数据进行异或
        for (size_t k = 0; k < input.size(); ++k) {
            i = (i + 1) % 256;
            j = (j + S[i]) % 256;

            // 交换S[i]和S[j]
            std::swap(S[i], S[j]);

            // 生成伪随机字节并与输入字节异或
            int t = (S[i] + S[j]) % 256;
            output[k] = input[k] ^ S[t];
        }

        return output;
    }

private:
    // 初始化密钥流
    void key_schedule(const std::string& key) {
        // 初始化S数组
        S.resize(256);
        for (int i = 0; i < 256; ++i) {
            S[i] = i;
        }

        // 将密钥扩展到S数组
        int j = 0;
        for (int i = 0; i < 256; ++i) {
            j = (j + S[i] + key[i % key.size()]) % 256;
            std::swap(S[i], S[j]);
        }
    }

    std::vector<int> S;  // RC4的状态数组
};