from collections import defaultdict
category_chapter_dict = defaultdict(list)

category_range_list = [
    [1, 1, 5],
    [2, 6, 14],
    [3, 15, 15],
    [4, 16, 24],
    [5, 25, 27],
    [6, 28, 38],
    [7, 39, 40],
    [8, 41, 43],
    [9, 44, 46],
    [10, 47, 49],
    [11, 50, 63],
    [12, 64, 67],
    [13, 68, 70],
    [14, 71, 71],
    [15, 72, 83],
    [16, 84, 85],
    [17, 86, 89],
    [18, 90, 92],
    [19, 93, 93],
    [20, 94, 96],
    [21, 97, 97],
    [22, 98, 98],
]

category_description_dict = {
    1: "第一类 活的动物及动物产品",
    2: "第二类 植物产品",
    3: "第三类 动植物油，及分解产品",
    4: "第四类 食品，饮料、酒及醋",
    5: "第五类 矿产品",
    6: "第六类 化学工业及相关工业产品",
    7: "第七类 塑料及其制品；橡胶及其制品",
    8: "第八类 生皮、皮革、毛皮； 包等",
    9: "第九类 木及木制品； 木炭；软木；稻草，秸秆",
    10: "第十类 木浆及其他纤维状纤维素浆；回收（废碎)纸或纸板；纸、纸板及其制品",
    11: "第十一类 纺织原料及纺织品",
    12: "第十二类 鞋、帽、伞、杖、鞭； 已加工的羽毛",
    13: "第十三类 石料、石膏、水泥、石棉、云母及类似",
    14: "第十四类 天然或羊脂珍珠、宝石",
    15: "第十五类 贱金属及其制品",
    16: "第十六类 机器、机械器具、电气设备及其零件；录音机、电视图像录制和重发设备",
    17: "第十七类 车辆、航空器、船舶及运输设备",
    18: "第十八类 光学、照相、电影等仪器",
    19: "第十九类 武器、弹药及其零件、附件",
    20: "第二十类 杂项制品",
    21: "第二十一类 艺术品、收藏品以及古物",
}

for category_range in category_range_list:
    category_chapter_dict[category_range[0]] = [x for x in range(category_range[1], category_range[2] + 1)]

chapter_category_dict = {vv: k for k, v in category_chapter_dict.items() for vv in v}


def get_category_range(category):
    for ranges in category_range_list:
        if ranges[0] == category:
            return ranges
    return [-1, -1, -1]


if __name__ == '__main__':
    print(get_category_range(15)[1])
