
#include <cmath>
#include <memory>

#include "ffcache.hpp"
#include "util.hpp"

FirefoxCacheEntry::FirefoxCacheEntry(const fs::path& path) {
    this->file_path = path;
    std::ifstream ifs(path, std::ios::binary);
    //meta start
    ifs.seekg(-4, std::ios::end);
    this->meta_end = ifs.tellg();
    ifs.read((char*)&meta_start, 4);
    endswap(&meta_start);

    if (this->meta_start > this->meta_end) {
        throw runtime_error("Invalid data structure");
    }

    //meta data
    int numHashChunks = std::ceil((double)meta_start / CHUNK_SIZE);
    ifs.seekg(meta_start + 4 + numHashChunks * 2, std::ios::beg);
    FirefoxMetaData::read(ifs, metadata);

    //key
    if (metadata.mKeySize > 0) {
        std::string key;
        key.resize(metadata.mKeySize);
        ifs.read(&key[0], metadata.mKeySize);
        this->key = key.substr(key.find(':') + 1);
    } else {
        this->key = "";
    }
    // ifs.seekg(1, std::ios::cur);
    this->map_start = this->meta_start + metadata.mKeySize + 1;  //ifs.tellg();
    ifs.close();
}

std::map<std::string, std::string> FirefoxCacheEntry::load_map() const {
    std::map<std::string, std::string> result;
    std::ifstream ifs(this->file_path, std::ios::binary);
    ifs.seekg(map_start, std::ios::beg);
    std::vector<std::string> vec;
    std::stringstream ss;
    char c;
    while (ifs.read(&c, 1), ifs.tellg() < this->meta_end) {
        if (c != '\0')
            ss << c;
        else {
            vec.push_back(ss.str());
            ss.str("");
            ss.clear();
        }
    }
    ifs.close();
    for (size_t i = 0; i + 1 < vec.size(); i += 2) {
        result[vec[i]] = vec[i + 1];
    }
    return result;
}

std::unique_ptr<std::vector<char>> FirefoxCacheEntry::get_data() const {
    auto ptr = std::make_unique<std::vector<char>>(this->meta_start);
    if (this->meta_start > 0) {
        std::ifstream ifs(this->file_path, std::ios::binary);
        ifs.read(&ptr->at(0), this->meta_start);
        ifs.close();
    }
    return ptr;
}

bool FirefoxCacheEntry::save(const std::string& __path) const {
    const auto ptr = this->get_data();

    if (ptr->size() > 0) {
        std::ofstream ofs{__path, std::ios::binary};
        ofs.write(&ptr->at(0), ptr->size());
        ofs.close();
        return true;
    } else {
        return false;
    }
}

HttpHeader FirefoxCacheEntry::get_header() const {
    return HttpHeader(this->load_map()["response-head"]);
}
