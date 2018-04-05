import pcl


p = pcl.PointCloud()
p.from_file("adquisicion1.pcd")
fil = p.make_statistical_outlier_filter()
fil.set_mean_k (50)
fil.set_std_dev_mul_thresh (1.0)
fil.filter().to_file("inliers2.pcd")