#include<bits/stdc++.h>
using namespace std;
#define long long ll;
void decode(string s){
    for(int i = 1 ; i <= 25 ; i++){
        string tmp = "";
        int key_number = i;
        for(int j = 0 ; j < s.length() ; j++){
            s[j] = char(int(s[j])+ (key_number % 26));
            tmp += s[j];
        }
        cout << tmp << endl;
    }
}
int main(void){
    string plain_text = "ynkooejcpdanqxeykjrbdofgkq";
    decode(plain_text);
}