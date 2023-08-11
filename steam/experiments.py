classes = [
    'platform_img win',
    'platform_img mac',
    'platform_img lin',
    'vr_supported'
]


def get_platforms(list_classes):
    platforms = []
    for item in list_classes:
        platform = item.split(' ')[-1]
        if platform == 'win':
            platforms.append('Windows')
        if platform == 'mac':
            platforms.append('Mac os')
        if platform == 'lin':
            platforms.append('Linux')
        if platform == 'vr_supported':
            platforms.append('VR Supported')
    return platforms


# get_platforms(classes)

reviews = [
    'search_review_summary mixed',
    'earch_review_summary positive',
    'search_review_summary negative',
    'None'
]


def get_reviews(list_reviews):
    reviews = []
    for item in list_reviews:
        review = item.split(' ')[-1]
        if review == 'positive':
            reviews.append('positive')
        elif review == 'negative':
            reviews.append('negative')
        elif review == 'mixed':
            reviews.append('mixed')
        else:
            reviews.append('None')
    return reviews


# get_reviews(reviews)
