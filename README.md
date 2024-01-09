# AutoGen 本地环境搭建 - Colab（1/2）

## 1. 背景

微软开源了 AutoGen 框架，专为大语言模型快速开发而设计。对于没有 OpenAI Key 的用户，尤其是白嫖党，存在一些挑战。考虑到 GitHub 上有许多开源的大模型，因此在本地部署这些大模型成为一个有趣的想法，以便进行 AutoGen 的开发。有关 AutoGen 的更多信息，请访问[官网](https://microsoft.github.io/autogen/)。

## 2. 需要解决的问题

1. 缺乏 GPU 环境：普通显卡或 PC 无法轻松部署大模型，而 Colab 提供免费的 T4 算力，为解决这一问题提供了可能性。
2. 非专业人士如何快速部署大模型：对于不了解量化等专业知识的用户，希望能够通过简单的操作或双击即可在本地部署大模型。GitHub 上已经有相关的工具可供使用。
3. 牛头能否对接马嘴：希望通过其他软件部署的大模型能够提供 API 接口，并且该接口的格式是否与 OpenAI 的一致。GitHub 上同样存在相关的工具可供参考。

## 3. 准备工作

1. [AutoGen](https://microsoft.github.io/autogen/) - AutoGen 框架。
2. [ollama](https://ollama.ai/) - 用于部署本地大模型，计划部署 mistral-7b。
3. [litellm](https://docs.litellm.ai/docs/) - 用于大模型协议转换，将其转换为 OpenAI 标准格式的 API。
4. 科学上网 - [***](https://github.com)

## 4. 实践思路

1. 先尝试用 ollama 部署大模型，测试能否跑起来。
2. 启动 litellm 进行协议转换。
3. 使用 AutoGen Demo 进行系统功能测试，查看系统是否正常工作。

## 5. 其他事项

1. Colab 记得切换笔记本环境为 GPU 环境-T4。

# 步骤 1：安装 ollama 并部署 mistral

```bash
# 主要命令
!curl https://ollama.ai/install.sh | sh
!nohup ollama serve &
!nohup ollama run mistral &
!curl -X POST http://localhost:11434/api/generate -d '{"model": "mistral","prompt":"Here is a story about llamas eating grass"}'

# 注：在 Colab 中，长期在后台运行程序会造成单元格阻塞，因此需要后台运行命令，调用命令时，使用如下方式 !nohup {cmd} &  ,查看命令的输出话用 !cat nohup.out
```

# 步骤 2：安装并启动 litellm

```bash
# 主要命令
!pip install litellm
# 下面的命令出错的话尝试 !pip install 'litellm[proxy]'
!nohup litellm --model ollama/mistral &
!cat nohup.out
!curl http://0.0.0.0:8000/models
```

# 步骤 3：安装并测试 AutoGen 能否正常工作

```bash
# 主要命令
!pip install pyautogen
llm_config = {
    'config_list':[
        {
            'model': "ollama/mistral",
            'api_key': "api",
            'base_url':'http://127.0.0.1:8000/'
        },
    ]
}
import autogen

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
)

user_proxy.initiate_chat(
    assistant,
    message="""现在是什么时间""",
)
```
