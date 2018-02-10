>> > mu, sigma = 0, 0.1  # mean and standard deviation
>> > s = np.random.normal(mu, sigma, 1000)

Verify
the
mean and the
variance:

>> > abs(mu - np.mean(s)) < 0.01
True

>> > abs(sigma - np.std(s, ddof=1)) < 0.01
True