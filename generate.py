from langchain.prompts import ChatPromptTemplate
from langchain_community.docstore import Wikipedia
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

def generate_script(subject, video_length, creativity, api_key):
    # 先写需要传入的标题以及需要ai生成的内容,是最后要变成的结果。
    title_template = ChatPromptTemplate.from_messages(
        [
            ('human','请为"{subject}"这个主题的视频想一个吸引人的标题。')
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            'human','''
            你是一位短视频频道的博主。
            根据以下标题和相关信息，为短视频频道写一个视频脚本。
            视频标题：{subject}，视频时长：{duration}分钟，生成的脚本长度尽量遵循视频时长的要求。
            要求抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也按照【开头，中间，结尾】分隔。
            整体内容的表达方式尽量轻松有趣，吸引年轻人。
            脚本内容可以结合以下维基百科搜索出的信息，仅作参考，只结合相关即可，对不相关的进行忽略：
            ```{wikipedia_search}```
            '''
        ]
    )
    # ai模型
    model = ChatOpenAI(api_key = api_key, temperature=creativity,
                       base_url = "https://free.v36.cm/v1")

    # 维基百科搜索
    wiki_client = Wikipedia()
    search = WikipediaAPIWrapper(wiki_client=wiki_client)
    search_result = search.run(subject)
    # 链
    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({'subject':subject}).content
    script = script_chain.invoke({'subject':subject, 'duration':video_length,'wikipedia_search':search_result}).content

    return  search_result, title, script
