
def sample_function():
    print("This is a sample function in utils.py")
    

# サブプロセスを利用した関数
def subprocess_function():
    import subprocess
    import platform
    
    try:
        # クロスプラットフォーム対応
        if platform.system() == "Windows":
            # Windows: shell=Trueでechoコマンドを実行
            result = subprocess.run('echo Hello from subprocess!', shell=True, capture_output=True, text=True)
        else:
            # Linux/Mac: リスト形式でechoコマンドを実行
            result = subprocess.run(['echo', 'Hello from subprocess!'], capture_output=True, text=True)
        
        print(result.stdout.strip())
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # 代替案：Pythonの標準出力を使用
        print("Hello from subprocess! (Python fallback)")


# サブプロセスでPythonファイルを実行する関数
def run_python_script():
    import subprocess
    try:
        # Pythonスクリプトをサブプロセスで実行
        result = subprocess.run(['python', 'app/func.py'], capture_output=True, text=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"Error running Python script: {e}")


if __name__ == "__main__":
    # sample_function()
    # subprocess_function()
    run_python_script()