# C++ Anti-Patterns (Google Style Guide)

## 1. Exceptions

Google C++ code does not use `throw`/`try`/`catch`. Most existing Google code
is not exception-safe, so introducing exceptions into new code creates
integration hazards with everything it calls or is called by.

```cpp
// Wrong
int Divide(int a, int b) {
  if (b == 0) throw std::invalid_argument("divide by zero");
  return a / b;
}

// Right — signal failure through the return channel
absl::StatusOr<int> Divide(int a, int b) {
  if (b == 0) {
    return absl::InvalidArgumentError("divide by zero");
  }
  return a / b;
}
```

## 2. Manual `new`/`delete` ownership tracking

Prefer smart pointers so ownership is explicit and lifetime is automatic.

```cpp
// Wrong
Foo* MakeFoo() {
  return new Foo();
}
void UseFoo() {
  Foo* f = MakeFoo();
  f->DoSomething();
  delete f;  // easy to forget, or to double-free on an error path
}

// Right
std::unique_ptr<Foo> MakeFoo() {
  return std::make_unique<Foo>();
}
void UseFoo() {
  auto f = MakeFoo();
  f->DoSomething();
  // destructor runs automatically
}
```

## 3. Non-`explicit` single-argument constructors

Without `explicit`, a single-argument constructor doubles as an implicit
conversion, which can silently do the wrong thing at a call site.

```cpp
// Wrong — Foo(int) enables silent int -> Foo conversions everywhere
class Foo {
 public:
  Foo(int size) : size_(size) {}
 private:
  int size_;
};
void Process(Foo f);
Process(42);  // Silently constructs a Foo — is that intended?

// Right
class Foo {
 public:
  explicit Foo(int size) : size_(size) {}
 private:
  int size_;
};
Process(Foo(42));  // Conversion must be explicit at the call site
```

## 4. C-style casts

```cpp
// Wrong — ambiguous whether this converts or reinterprets
double d = 3.9;
int i = (int)d;
Base* b = (Base*)derived_ptr;

// Right
int i = static_cast<int>(d);
Base* b = static_cast<Base*>(derived_ptr);
```

## 5. RTTI-based type-switch decision trees

```cpp
// Wrong
if (typeid(*shape) == typeid(Circle)) {
  DrawCircle(shape);
} else if (typeid(*shape) == typeid(Square)) {
  DrawSquare(shape);
}

// Right — virtual dispatch
class Shape {
 public:
  virtual void Draw() const = 0;
};
class Circle : public Shape {
 public:
  void Draw() const override { /* ... */ }
};
shape->Draw();
```

## 6. Macros defining API surface

```cpp
// Wrong — macro expands into class members; breaks tooling and readability
#define DECLARE_GETTERS(Type, name) \
  Type name() const { return name##_; } \
  void set_##name(Type v) { name##_ = v; }

class Widget {
 public:
  DECLARE_GETTERS(int, width)
};

// Right — write it out, or use a template/constexpr helper instead
class Widget {
 public:
  int width() const { return width_; }
  void set_width(int width) { width_ = width; }
 private:
  int width_ = 0;
};
```

## 7. Non-trivially-destructible static/global variables

```cpp
// Wrong — std::string has a non-trivial destructor; destruction order
// across translation units is unspecified, risking use-after-destroy.
const std::string kFoo = "foo";

// Right — use a string literal (already static storage duration) or a
// deliberately-leaked heap object via a function-local static.
constexpr char kFoo[] = "foo";

const std::string& GetFoo() {
  static const std::string& foo = *new std::string("foo");
  return foo;
}
```

## 8. `using namespace` directives

```cpp
// Wrong — pollutes the namespace, can silently change overload resolution
using namespace std;

// Right — qualify explicitly, or bring in only the specific names you need
// in a .cc file (never at namespace scope in a header)
using ::foo::Bar;
```

## 9. Virtual calls in constructors/destructors

```cpp
// Wrong — virtual calls in a constructor never dispatch to a subclass
// override, which surprises readers and silently breaks when a class is
// later subclassed.
class Base {
 public:
  Base() { Init(); }        // calls Base::Init, never Derived::Init
  virtual void Init() {}
};

// Right — use a factory function or separate Init() called after
// construction completes.
class Base {
 public:
  static std::unique_ptr<Base> Create() {
    auto obj = std::make_unique<Base>();
    obj->Init();
    return obj;
  }
  virtual void Init() {}
};
```

## 10. Unsigned types to express "never negative"

```cpp
// Wrong — underflow wraps silently instead of erroring
uint32_t remaining = total - used;  // wraps to a huge number if used > total

// Right — use a signed type and assert/check the invariant explicitly
int64_t remaining = total - used;
CHECK_GE(remaining, 0);
```

## 11. Unnecessary post-increment

```cpp
// Wrong — makes a throwaway copy of the pre-increment value
for (auto it = container.begin(); it != container.end(); it++) { ... }

// Right
for (auto it = container.begin(); it != container.end(); ++it) { ... }
```

## 12. Overloading banned operators / user-defined literals

```cpp
// Wrong — banned outright
Foo operator&&(const Foo& a, const Foo& b);
constexpr Foo operator"" _foo(unsigned long long v);

// Right — use named functions instead
Foo LogicalAnd(const Foo& a, const Foo& b);
constexpr Foo MakeFoo(unsigned long long v);
```
