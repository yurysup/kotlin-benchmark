package test

import kotlinx.benchmark.*
import java.util.concurrent.*

@State(Scope.Benchmark)
//@Warmup(iterations = 1)
@BenchmarkMode(Mode.AverageTime)
//@Measurement(iterations = 1, time = 1)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
class FibonacciBenchmark {

    @Param("10", "20")
    var n: Int = 0

    @Benchmark
    fun compute_fibonacci() {
        fibonacci(n)
    }
}