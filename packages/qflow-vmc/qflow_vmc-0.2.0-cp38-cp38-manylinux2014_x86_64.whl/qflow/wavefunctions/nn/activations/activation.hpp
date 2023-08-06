#pragma once

#include "definitions.hpp"

#include <Eigen/Dense>

namespace activation
{
class ActivationFunction
{
public:
    virtual Matrix evaluate(const MatrixRef& x) const      = 0;
    virtual Matrix derivative(const MatrixRef& x) const    = 0;
    virtual Matrix dblDerivative(const MatrixRef& x) const = 0;
};

template <typename F, typename DF, typename DDF>
class DerivedActivationFunction : public ActivationFunction
{
private:
    const F   f {};
    const DF  df {};
    const DDF ddf {};

public:
    Matrix evaluate(const MatrixRef& x) const override { return x.unaryExpr(f); }

    Matrix derivative(const MatrixRef& y) const override { return y.unaryExpr(df); }

    Matrix dblDerivative(const MatrixRef& y) const override { return y.unaryExpr(ddf); }
};

namespace functors
{
namespace relu
{
struct eval
{
    constexpr Real operator()(Real x) const { return x > 0 ? x : 0; }
};
struct deriv
{
    constexpr Real operator()(Real y) const { return y > 0 ? 1 : 0; }
};
struct dblDeriv
{
    constexpr Real operator()(Real y) const
    {
        (void) y;
        return 0;
    }
};
}  // namespace relu

namespace identity
{
struct eval
{
    constexpr Real operator()(Real x) const { return x; }
};
struct deriv
{
    constexpr Real operator()(Real y) const
    {
        (void) y;
        return 1;
    }
};
struct dblDeriv
{
    constexpr Real operator()(Real y) const
    {
        (void) y;
        return 0;
    }
};
}  // namespace identity

namespace sigmoid
{
struct eval
{
    constexpr Real operator()(Real x) const { return 1 / (1 + std::exp(-x)); }
};
struct deriv
{
    constexpr Real operator()(Real y) const { return y * (1 - y); }
};
struct dblDeriv
{
    constexpr Real operator()(Real y) const { return y * (1 - y) * (1 - 2 * y); }
};
}  // namespace sigmoid

namespace tanh
{
struct eval
{
    constexpr Real operator()(Real x) const { return std::tanh(x); }
};
struct deriv
{
    constexpr Real operator()(Real y) const { return 1 - y * y; }
};
struct dblDeriv
{
    constexpr Real operator()(Real y) const
    {
        Real x = std::atanh(y);
        return -2 * y / square(std::cosh(x));
    }
};
}  // namespace tanh

namespace exponential
{
struct eval
{
    constexpr Real operator()(Real x) const { return std::exp(x); }
};
struct deriv
{
    constexpr Real operator()(Real y) const { return y; }
};
struct dblDeriv
{
    constexpr Real operator()(Real y) const { return y; }
};
}  // namespace exponential

}  // namespace functors

using ReluActivation     = DerivedActivationFunction<functors::relu::eval,
                                                 functors::relu::deriv,
                                                 functors::relu::dblDeriv>;
using IdentityActivation = DerivedActivationFunction<functors::identity::eval,
                                                     functors::identity::deriv,
                                                     functors::identity::dblDeriv>;
using SigmoidActivation  = DerivedActivationFunction<functors::sigmoid::eval,
                                                    functors::sigmoid::deriv,
                                                    functors::sigmoid::dblDeriv>;
using TanhActivation     = DerivedActivationFunction<functors::tanh::eval,
                                                 functors::tanh::deriv,
                                                 functors::tanh::dblDeriv>;
using ExponentialActivation
    = DerivedActivationFunction<functors::exponential::eval,
                                functors::exponential::deriv,
                                functors::exponential::dblDeriv>;

extern ReluActivation        relu;
extern IdentityActivation    identity;
extern SigmoidActivation     sigmoid;
extern TanhActivation        tanh;
extern ExponentialActivation exponential;

}  // namespace activation
