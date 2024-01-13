# environment_setup.py

import subprocess
import time

def initialize_environment():
    print('开始初始化Autogen运行环境。')
    llm_model = 'mistral'

    ollama_install_file = ['curl', '-o', 'ollama_install.sh', 'https://ollama.ai/install.sh']
    ollama_install = ['sh', 'ollama_install.sh']
    ollama_server_start = ['ollama', 'serve']
    ollama_pull_model = ['ollama', 'pull', llm_model]
    ollama_list_model = ['ollama', 'list']

    pip_install_dependency = ['pip', 'install', 'litellm[proxy]', 'pyautogen']

    litellm_server_start = ['litellm', '--model', f'ollama/{llm_model}']

    with open('log.txt', 'w') as log:
        # Install ollama and start ollama server
        print('步骤1: 开始安装ollama.')
        subprocess.Popen(ollama_install_file, stdout=log, stderr=log).wait()
        subprocess.Popen(ollama_install, stdout=log, stderr=log).wait()
        print('步骤1: ollama安装完成.')

        # Ollama server start
        print('步骤2: 启动ollama服务')
        subprocess.Popen(ollama_server_start, stdout=log, stderr=log)
        time.sleep(5)
        print('步骤2: ollama服务启动完成')

        # Ollama pull llm model
        print(f'步骤3: 拉取大模型镜像文件-{llm_model}，需要等待一定时间，可查看log文件了解进度')
        subprocess.Popen(ollama_pull_model, stdout=log, stderr=log).wait()
        print(f'步骤3: 模型文件拉取完成')

        # Pip install dependency
        print('步骤4: 安装其他依赖：litellm autogen')
        subprocess.Popen(pip_install_dependency, stdout=log, stderr=log).wait()
        print('步骤4: 依赖安装完成')

        # Litellm server start
        print('步骤5: 启动litellm服务')
        subprocess.Popen(litellm_server_start, stdout=log, stderr=log)
        time.sleep(5)
        print('步骤5: litellm服务启动完成')

def check():
    import autogen
    llm_config = {
        'config_list': [
            {
                'model': "ollama/mistral",
                'api_key': "api",
                'base_url': 'http://127.0.0.1:8000/'
            },
        ]
    }

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
    )
    print('步骤6: 验证环境是否正常，查看机器人是否能够回复消息')
    user_proxy.initiate_chat(
        assistant,
        message="""现在是什么时间""",
    )
    print('步骤6: 环境ok，开始你的表演')

if __name__ == '__main__':
    initialize_environment()
    check()
