function res = numerical_differentiation(f, x0, h)
% =========================================================================
% خوارزمية صيغ التفاضل العددي بصيغ تايلور (Numerical Differentiation)
% مادة: التحليل العددي (Numerical Analysis)
% =========================================================================
% الوظيفة:
%   تقريب المشتقات الأولى والثانية للدالة f(x) عند النقطة x0 باستخدام:
%   1. الفروق الأمامية (Forward Difference): O(h)
%   2. الفروق الخلفية (Backward Difference): O(h)
%   3. الفروق المركزية (Central Difference): O(h^2) (الأدق للمشتقة الأولى)
%   4. المشتقة الثانية المركزية (Second Derivative): O(h^2)
%
% المدخلات (Inputs):
%   f  : الدالة الرياضية كـ function handle، مثال: @(x) sin(x)
%   x0 : النقطة المطلوب حساب المشتقة عندها
%   h  : خطوة التفاضل (افتراضياً: 0.01)
%
% المخرجات (Outputs):
%   res : هيكل struct يحوي نتائج جميع الصيغ المقربة
% =========================================================================

    if nargin < 1 || isempty(f), f = @(x) sin(x); end
    if nargin < 2 || isempty(x0), x0 = 1.0; end
    if nargin < 3 || isempty(h), h = 0.01; end

    if ischar(f) || isstring(f), f = str2func(['@(x) ' char(f)]); end

    fx0 = f(x0);
    fx_plus = f(x0 + h);
    fx_minus = f(x0 - h);

    % 1. الفروق الأمامية
    d_forward = (fx_plus - fx0) / h;
    % 2. الفروق الخلفية
    d_backward = (fx0 - fx_minus) / h;
    % 3. الفروق المركزية
    d_central = (fx_plus - fx_minus) / (2 * h);
    % 4. المشتقة الثانية
    d2_central = (fx_plus - 2 * fx0 + fx_minus) / (h^2);

    res.forward = d_forward;
    res.backward = d_backward;
    res.central = d_central;
    res.second_order = d2_central;

    fprintf('\n=================================================================\n');
    fprintf('  صيغ التفاضل العددي (Numerical Differentiation)\n');
    fprintf('=================================================================\n');
    fprintf('النقطة x0 = %.4f,  الخطوة h = %.4f\n', x0, h);
    fprintf('f(x0 - h) = %10.6f\n', fx_minus);
    fprintf('f(x0)     = %10.6f\n', fx0);
    fprintf('f(x0 + h) = %10.6f\n', fx_plus);
    fprintf('-----------------------------------------------------------------\n');
    fprintf('1. الفروق الأمامية (Forward)   : f''(x0) ≈ %12.6f  [خطأ O(h)]\n', d_forward);
    fprintf('2. الفروق الخلفية (Backward)  : f''(x0) ≈ %12.6f  [خطأ O(h)]\n', d_backward);
    fprintf('3. الفروق المركزية (Central)   : f''(x0) ≈ %12.6f  [خطأ O(h^2) الأدق]\n', d_central);
    fprintf('4. المشتقة الثانية (f'''' Central): f''''(x0) ≈ %12.6f  [خطأ O(h^2)]\n', d2_central);
    fprintf('=================================================================\n');
end
