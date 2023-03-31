#include <vector>
#include <iostream>
#include <stdexcept>
#include <random>

template<typename T>
class NDArray {
private:
    std::vector<T> data;
    std::vector<int> shape;

public:
    NDArray(std::vector<int>& shape)
        : shape(shape) {
        int size = 1;
        for (int dim : shape) {
            size *= dim;
        }
        data.resize(size);
    }

    NDArray(std::vector<int>& shape, T init_val)
        : NDArray(shape) {
        std::fill(data.begin(), data.end(), init_val);
    }

    static NDArray<T> zeros(std::vector<int>& shape) {
        NDArray<T> array(shape);
        std::fill(array.data.begin(), array.data.end(), T(0));
        return array;
    }

    static NDArray<T> ones(std::vector<int>& shape) {
        NDArray<T> array(shape);
        std::fill(array.data.begin(), array.data.end(), T(1));
        return array;
    }

    static NDArray<T> random(std::vector<int>& shape) {
        NDArray<T> array(shape);
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<T> dist(0.0, 1.0);
        for (T& val : array.data) {
            val = dist(gen);
        }
        return array;
    }

    int size() {
        return data.size();
    }

    std::vector<int>& get_shape() {
        return shape;
    }

    int ndim()  { return shape.size(); }

    T& get(std::vector<int>& indices) {
        int flat_index = nindex_to_index(indices);
        return data[flat_index];
    }

    void set(std::vector<int>& indices, T value) {
        int flat_index = nindex_to_index(indices);
        data[flat_index] = value;
    }

    NDArray<T> operator+( NDArray<T>& other)  {
        NDArray<T> result(shape);
        for (int i = 0; i < size(); ++i) {
            result.data[i] = data[i] + other.data[i];
        }
        return result;
    }

    NDArray<T> operator-( NDArray<T>& other)  {
        NDArray<T> result(shape);
        for (int i = 0; i < size(); ++i) {
            result.data[i] = data[i] - other.data[i];
        }
        return result;
    }

    NDArray<T> operator*( NDArray<T>& other)  {
        NDArray<T> result(shape);
        for (int i = 0; i < size(); ++i) {
            result.data[i] = data[i] * other.data[i];
        }
        return result;
    }

    NDArray<T> operator/( NDArray<T>& other)  {
        NDArray<T> result(shape);
        for (int i = 0; i < size(); ++i) {
            if (other.data[i] == T(0)) {
                throw std::invalid_argument("Division by zero");
            }
            result.data[i] = data[i] / other.data[i];
        }
        return result;
    }

    NDArray<T> min(int dimension)  {
        std::vector<int> new_shape(shape);
        new_shape.erase(new_shape.begin() + dimension);
        NDArray<T> result(new_shape);
        std::vector<int> indices(shape.size(), 0);
        for (int i = 0; i < result.size(); ++i) {
            int min_val = std::numeric_limits<T>::max();
            indices[dimension] = 0;
            for (int j = 0; j < shape[dimension]; ++j) {
                int flat_index = nindex_to_index(indices);
                min_val = std::min(min_val, data[flat_index]);
                ++indices[dimension];
            }
            result.data[i] = min_val;
            increment_indices(indices, shape);
        }
        return result;
    }

    NDArray<T> max(int dimension)  {
        std::vector<int> new_shape(shape);
        new_shape.erase(new_shape.begin() + dimension);
        NDArray<T> result(new_shape);
        std::vector<int> indices(shape.size(), 0);
        for (int i = 0; i < result.size(); ++i) {
            int max_val = std::numeric_limits<T>::min();
            indices[dimension] = 0;
            for (int j = 0; j < shape[dimension]; ++j) {
                int flat_index = nindex_to_index(indices);
                max_val = std::max(max_val, data[flat_index]);
                ++indices[dimension];
            }
            result.data[i] = max_val;
            increment_indices(indices, shape);
        }
        return result;
    }

    NDArray<T> mean(int dimension)  {
        std::vector<int> new_shape(shape);
        new_shape.erase(new_shape.begin() + dimension);
        NDArray<T> result(new_shape);
        std::vector<int> indices(shape.size(), 0);
        for (int i = 0; i < result.size(); ++i) {
            T sum = T(0);
            indices[dimension] = 0;
            for (int j = 0; j < shape[dimension]; ++j) {
                int flat_index = nindex_to_index(indices);
                sum += data[flat_index];
                ++indices[dimension];
            }
            result.data[i] = sum / shape[dimension];
            increment_indices(indices, shape);
        }
        return result;
    }

    NDArray<T> transpose()  {
        if (shape.size() <= 1) {
            return *this;
        }
        std::vector<int> new_shape(shape.rbegin(), shape.rend());
        NDArray<T> result(new_shape);
        std::vector<int> indices(new_shape.size(), 0);
        for (int i = 0; i < size(); ++i) {
            int flat_index = nindex_to_index(indices);
            result.data[i] = data[flat_index];
            increment_indices(indices, new_shape);
        }
        return result;
    }

    NDArray<T> matmul( NDArray<T>& other)  {
        NDArray<T> result({shape[0], other.shape[1]});
        for (int i = 0; i < shape[0]; ++i) {
            for (int j = 0; j < other.shape[1]; ++j) {
                T sum = T(0);
                for (int k = 0; k < shape[1]; ++k) {
                    sum += get({i, k}) * other.get({k, j});
                }
                result(i, j) = sum;
            }
        }
        return result;
    }

    void print() {
        std::cout << "[";
        for (int i = 0; i < size(); ++i) {
            std::vector<int> indices = index_to_nindex(i, shape);
            std::cout << get(indices);
            if (i != size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }

private:
    int nindex_to_index( std::vector<int>& indices) {
        int flat_index = 0;
        int shift = 1;
        for (int i = indices.size() - 1; i >= 0; --i) {
            flat_index += indices[i] * shift;
            shift *= shape[i];
        }
        return flat_index;
    }

    std::vector<int> index_to_nindex(int index, std::vector<int>& shape) {
        std::vector<int> result(shape.size());
        for (int i = shape.size() - 1; i >= 0; --i) {
            result[i] = index % shape[i];
            index /= shape[i];
        }
        return result;
    }

    void increment_indices(std::vector<int>& indices, std::vector<int> max_indices) {
        int n_dims = indices.size();
        int carry = 1;
        for (int i = n_dims - 1; i >= 0; i--) {
            indices[i] += carry;
            if (indices[i] >= max_indices[i]) {
                indices[i] = 0;
                carry = 1;
            } else {
                carry = 0;
                break;
            }
        }
    }
};