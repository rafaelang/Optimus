from pyspark.sql import DataFrame

from optimus import PYSPARK_NUMERIC_TYPES
from optimus.plots import plot_scatterplot, plot_boxplot, plot_freq, plot_hist, plot_correlation
from optimus.helpers.decorators import add_attr
from optimus.helpers.columns import parse_columns, check_column_numbers


def plot(self):
    @add_attr(plot)
    def hist(columns=None, buckets=10, output_image_format=None, ouput_path=None):
        """
        Plot histogram
        :param columns: Columns to be printed
        :param buckets: Number of buckets
        :param output_image_format:
        :param ouput_path:
        :return:
        """
        columns = parse_columns(self, columns, filter_by_column_dtypes=PYSPARK_NUMERIC_TYPES)
        check_column_numbers(columns, "*")

        for col_name in columns:
            data = self.cols.hist(col_name, buckets)
            plot_hist({col_name: data}, output=output_image_format, path=ouput_path)

    @add_attr(plot)
    def scatter(columns=None, buckets=30, output_image_format=None, output_path=None):
        """
        Plot boxplot
        :param columns: columns to be printed
        :param buckets: number of buckets
        :param output_image_format:
        :param output_path:
        :return:
        """
        columns = parse_columns(self, columns, filter_by_column_dtypes=PYSPARK_NUMERIC_TYPES)
        check_column_numbers(columns, "*")

        data = self.cols.scatter(columns, buckets)
        plot_scatterplot(data, output=output_image_format, path=output_path)

    @add_attr(plot)
    def box(columns=None, output_image_format=None, output_path=None):
        """
        Plot boxplot
        :param columns: Columns to be printed
        :param output_image_format:
        :param output_path:
        :return:
        """
        columns = parse_columns(self, columns, filter_by_column_dtypes=PYSPARK_NUMERIC_TYPES)
        check_column_numbers(columns, "*")

        for col_name in columns:
            stats = self.cols.boxplot(col_name)
            plot_boxplot({col_name: stats}, output=output_image_format, path=output_path)

    @add_attr(plot)
    def frequency(columns=None, buckets=10, output_image_format=None, output_path=None):
        """
        Plot frequency chart
        :param columns: Columns to be printed
        :param buckets: Number of buckets
        :param output_image_format:
        :param output_path:
        :return:
        """
        columns = parse_columns(self, columns)

        for col_name in columns:
            data = self.cols.frequency(col_name, buckets)
            plot_freq(data, output=output_image_format, path=output_path)

    @add_attr(plot)
    def correlation(col_name, method="pearson", output_image_format=None, output_path=None):
        """
        Compute the correlation matrix for the input data set of Vectors using the specified method. Method
        mapped from pyspark.ml.stat.Correlation.
        :param col_name: The name of the column for which the correlation coefficient needs to be computed.
        :param method: String specifying the method to use for computing correlation. Supported: pearson (default),
        spearman.
        :param output_image_format: Output image format
        :param output_path: Output path
        :return: Heatmap plot of the corr matrix using seaborn.
        """

        corr = self.correlation(col_name, method, output="array")
        plot_correlation(corr, output=output_image_format, path=output_path)

    return plot


DataFrame.plot = property(plot)
