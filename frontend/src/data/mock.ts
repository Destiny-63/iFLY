// 用户数据（levelKey 用于多语种，与 sidebar.level_* 对应）
export const userData = {
  id: 1,
  name: 'Hu',
  avatar: '训',
  email: 'demo@iflytek.com',
  avatarUrl: '',
  /** 等级展示 key，对应 locale sidebar.level_novice / level_primary / level_intermediate / level_advanced */
  levelKey: 'novice' as const,
}

// 题型数据：character=字 word=词语 sentence=句子 article=文章
export const questionTypes = [
  { id: 'character', name: '字', icon: '📝' },
  { id: 'word', name: '词语', icon: '💬' },
  { id: 'sentence', name: '句子', icon: '📋' },
  { id: 'article', name: '文章', icon: '📄' },
]

// 功能模块数据（根据文档）
export const mainModules = [
  { id: 'mock-exam', name: '模拟考试', icon: 'exam' },
  { id: 'practice', name: '专项训练', icon: 'practice' },
  { id: 'error-notebook', name: '错题本', icon: 'notebook' },
  { id: 'question-bank', name: 'PSC考试题库', icon: 'bank' },
]

// PSC 考试部分（5 项）
export const pscParts = [
  { id: 'singleCharacterReading', name: '读单音节字词', description: '100个单音节字词，音素级调制错误分析，识别错误与缺陷音' },
  { id: 'wordReading', name: '读多音节词语', description: '50个多音节词语，声调变化规则（轻声、儿化、多音节重音）' },
  { id: 'choiceJudgment', name: '选择判断', description: '词语判断、量词名词搭配、语序或表达形式判断' },
  { id: 'passageReading', name: '朗读短文', description: '400字短文朗读，停顿与重音分析，句切分示例与朗读示范' },
  { id: 'topicSpeaking', name: '命题说话', description: '给定话题单向说话3分钟，话题分类，每类提供阅读与引用材料' },
]

// 错题本分类
export const errorNotebookCategories = [
  { id: 'grading-errors', name: '评分错误', description: '根据评分结果提取的错误' },
  { id: 'favorites', name: '收藏夹', description: '自动整理，定期复习' },
]

// 题型专项题目库默认数据（当 /data/questions.json 加载失败时使用）
// 正式题目请配置 frontend/public/data/questions.json，支持题目内容、指导重点、音频源等
import type { QuestionBank } from '@/types/questions'

export const fallbackQuestionBank: QuestionBank = {
  character: [
    { id: 'character-1', title: '单字声调', content: '你', guidance: '请重点关注声调', audioExampleUrl: '', prompt: '请重点关注声调', difficulty: '初级', tags: ['声调'] },
    { id: 'character-2', title: '单字声母', content: '谢', guidance: '请重点关注声母', audioExampleUrl: '', prompt: '请重点关注声母', difficulty: '初级', tags: ['声母'] },
  ],
  word: [
    { id: 'word-1', title: '基础问候', content: '你好', guidance: '请重点关注声调', audioExampleUrl: '', prompt: '请重点关注声调', difficulty: '初级', tags: ['问候', '声调'] },
    { id: 'word-2', title: '礼貌用语', content: '谢谢', guidance: '请重点关注声母和韵母', audioExampleUrl: '', prompt: '请重点关注声母和韵母', difficulty: '初级', tags: ['礼貌', '声韵母'] },
  ],
  sentence: [
    { id: 'sentence-3', title: '天气话题', content: '今天天气怎么样？', guidance: '请重点关注声调和流畅度，以及句末疑问语调。', audioExampleUrl: '/audio/examples/read_sentence_cn.mp3', prompt: '请重点关注声调和流畅度', difficulty: '初级', tags: ['日常', '语调'], segments: ['今天', '天气', '怎么样？'] },
    { id: 'sentence-1', title: '祈使句', content: '请把窗户打开。', guidance: '请重点关注轻声「户」和整体祈使句的语调。', audioExampleUrl: '', prompt: '请重点关注轻声和语调', difficulty: '初级', tags: ['祈使', '轻声'], segments: ['请把', '窗户', '打开。'] },
    { id: 'sentence-2', title: '学习表达', content: '我喜欢学习普通话。', guidance: '请重点关注发音准确性，尤其是「喜欢」「普通话」的连读。', audioExampleUrl: '', prompt: '请重点关注发音准确性', difficulty: '初级', tags: ['学习', '连读'], segments: ['我', '喜欢', '学习', '普通话。'] },
  ],
  article: [
    { id: 'article-1', title: '白杨礼赞', content: '那是力争上游的一种树，笔直的干，笔直的枝。它的干通常是丈把高，像加过人工似的，一丈以内绝无旁枝。它所有的丫枝一律向上，而且紧紧靠拢，也像加过人工似的，成为一束，绝不旁逸斜出。它的宽大的叶子也是片片向上，几乎没有斜生的，更不用说倒垂了。它的皮光滑而有银色的晕圈，微微泛出淡青色。这是虽在北方的风雪的压迫下却保持着倔强挺立的一种树。', guidance: '请重点关注语流和停顿，句间换气自然，注意排比句的节奏。', audioExampleUrl: '', prompt: '请重点关注语流、停顿与节奏', difficulty: '中级', tags: ['散文', '语流'], segments: ['那是力争上游的一种树，', '笔直的干，', '笔直的枝。', '它的干通常是丈把高，', '像加过人工似的，', '一丈以内绝无旁枝。', '它所有的丫枝一律向上，', '而且紧紧靠拢，', '也像加过人工似的，', '成为一束，', '绝不旁逸斜出。', '它的宽大的叶子也是片片向上，', '几乎没有斜生的，', '更不用说倒垂了。', '它的皮光滑而有银色的晕圈，', '微微泛出淡青色。', '这是虽在北方的风雪的压迫下却保持着倔强挺立的一种树。'] },
  ],
}

// 提示词模板
export const guidancePrompts = {
  character: '请重点关注每个字的发音准确性，特别是声母、韵母和声调。',
  word: '请重点关注词语的流畅度、声调变化和整体语调。',
  sentence: '请重点关注句子的流畅度、声调变化和整体语调。',
  article: '请重点关注语流的连贯性、停顿的合理性以及整体表达的完整性。',
}
