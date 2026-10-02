function [root, T] = false_position(f, a, b, tol, max_iter)
% =========================================================================
% خوارزمية طريقة الموضع الخاطئ (False Position / Regula Falsi Method)
% مادة: التحليل العددي (Numerical Analysis)
% =========================================================================
% الوظيفة:
%   إيجاد الجذر الحقيقي للمعادلة f(x) = 0 عن طريق رسم وتر يربط النقطتين
%   (a, f(a)) و (b, f(b)) وحساب نقطة تقاطعه مع محور السينات x.
%
% الصيغة الرياضية:
%   p = b - (f(b) * (b - a)) / (f(b) - f(a))
%   أو بصيغة التبسيط:
%   p = (a * f(b) - b * f(a)) / (f(b) - f(a))
%
% المدخلات (Inputs):
%   f        : دالة رياضية كـ function handle، مثال: @(x) x.^3 - x - 2
%   a        : بداية فترة الحصر
%   b        : نهاية فترة الحصر
%   tol      : الدقة المطلوبة (افتراضياً: 1e-4)
%   max_iter : أقصى عدد تكرارات (افتراضياً: 50)
%
% المخرجات (Outputs):
%   root     : القيمة التقريبية للجذر المحسوب
%   T        : جدول التكرارات
% =========================================================================

    % 1. القيم الافتراضية عند التشغيل المباشر
    if nargin < 1 || isempty(f), f = @(x) x.^3 - x - 2; end
    if nargin < 2 || isempty(a), a = 1.0; end
    if nargin < 3 || isempty(b), b = 2.0; end
    if nargin < 4 || isempty(tol), tol = 1e-4; end
    if nargin < 5 || isempty(max_iter), max_iter = 50; end

    if ischar(f) || isstring(f)
        f = str2func(['@(x) ' char(f)]);
    end

    fprintf('\n=================================================================\n');
    fprintf('  طريقة الموضع الخاطئ (False Position / Regula Falsi)\n');
    fprintf('=================================================================\n');
    fprintf('الفترة الابتدائية: [%.4f, %.4f]\n', a, b);
    fprintf('الدقة المطلوبة: %e\n', tol);
    fprintf('-----------------------------------------------------------------\n');

    if a >= b
        error('خطأ: يجب أن تكون بداية الفترة a أصغر من نهايتها b.');
    end

    fa = f(a);
    fb = f(b);

    if abs(fa) < 1e-14, root = a; return; end
    if abs(fb) < 1e-14, root = b; return; end

    if fa * fb > 0
        error('خطأ: شرط الحصر غير محقق f(a)*f(b) > 0. الدالة لا تغير إشارتها في الفترة.');
    end

    fprintf('%-4s | %-9s | %-9s | %-9s | %-10s | %-10s | %-10s\n', ...
        'n', 'a', 'b', 'p (الجذر)', 'f(a)', 'f(p)', 'الخطأ |p - p_prev|');
    fprintf('-----------------------------------------------------------------\n');

    table_data = [];
    p_prev = a;

    for n = 1:max_iter
        fa = f(a);
        fb = f(b);

        denom = fb - fa;
        if abs(denom) < 1e-15
            error('خطأ: المقام f(b) - f(a) قريب جداً من الصفر (قسمة على صفر).');
        end

        % قانون نقطة تقاطع الوتر مع المحور الأفقي
        p = b - (fb * (b - a)) / denom;
        fp = f(p);

        if n == 1
            err = abs(b - a);
        else
            err = abs(p - p_prev);
        end

        fprintf('%-4d | %9.5f | %9.5f | %9.5f | %10.5f | %10.5f | %10.5e\n', ...
            n, a, b, p, fa, fp, err);

        table_data = [table_data; n, a, b, p, fa, fp, err]; %#ok<AGROW>

        if err < tol || abs(fp) < 1e-12
            fprintf('-----------------------------------------------------------------\n');
            fprintf('✓ تم الوصول للحل بنجاح عند التكرار n = %d\n', n);
            fprintf('✓ الجذر التقريبي: x ≈ %.6f\n', p);
            fprintf('✓ قيمة الدالة عند الجذر: f(x) = %e\n', fp);
            root = p;
            T = table_data;
            return;
        end

        if fa * fp < 0
            b = p;
        else
            a = p;
        end
        p_prev = p;
    end

    root = p;
    T = table_data;
    warning('تم بلوغ الحد الأقصى للتكرارات دون الوصول للدقة التامة.');
end
