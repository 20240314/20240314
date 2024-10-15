import numpy as np
import matplotlib.pyplot as plt

def linear_regression(X, Y):
    # X는 중간고사 점수, Y는 기말고사 점수
    # X에 절편을 위한 열을 추가 (즉, 1을 추가해줌)
    X_b = np.c_[np.ones((X.shape[0], 1)), X]  # X_b: (n, 2) [1, X] 형식
    theta = np.linalg.pinv(X_b).dot(Y)  # 회귀계수 계산 (유사역행렬을 사용하여 구함)
    return theta  # [절편, 기울기] 반환

if __name__ == '__main__':
    midterm_range = np.array([0, 125])
    final_range = np.array([0, 100])

    # Load score data
    class_kr = np.loadtxt('data/class_score_kr.csv', delimiter=',')
    class_en = np.loadtxt('data/class_score_en.csv', delimiter=',')
    data = np.vstack((class_kr, class_en))

    # Estimate a line, final = slope * midterm + y_intercept
    X = data[:, 0]  # 중간고사 점수
    Y = data[:, 1]  # 기말고사 점수

    # 선형 회귀 수행
    theta = linear_regression(X, Y)
    line = [theta[1], theta[0]]

    # Predict scores
    final = lambda midterm: line[0] * midterm + line[1]
    while True:
        try:
            given = input('Q) Please input your midterm score (Enter or -1: exit)? ')
            if given == '' or float(given) < 0:
                break
            print(f'A) Your final score is expected to {final(float(given)):.3f}.')
        except Exception as ex:
            print(f'Cannot answer the question. (message: {ex})')
            break

    # Plot scores and the estimated line
    plt.figure()
    plt.plot(data[:,0], data[:,1], 'r.', label='The given data')
    plt.plot(midterm_range, final(midterm_range), 'b-', label='Prediction')
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim(midterm_range)
    plt.ylim(final_range)
    plt.grid()
    plt.legend()
    plt.show()
