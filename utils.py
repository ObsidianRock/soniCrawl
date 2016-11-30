from urllib import parse, robotparser

def same_domain(url1, url2):
    return parse.urlparse(url1).netloc == parse.urlparse(url2).netloc

def get_robot_txt(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, '/robot.txt'))
    rp.read()
    return rp

def normalize(seed_url, link):
    link, _ = parse.urldefrag(link) # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)
