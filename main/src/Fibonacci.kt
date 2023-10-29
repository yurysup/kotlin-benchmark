package test

/* 
fun fibonacci(n: Int): Long {
    if (n <= 1) return n
    return fibonacci(n - 1) + fibonacci(n - 2)
}
*/


fun fibonacci(n: Int): Long {
    if (n <= 1) return n.toLong()
    var a = 0L
    var b = 1L
    for (i in 2..n) {
        val temp = a + b
        a = b
        b = temp
    }
    return b
}