function [root, T] = newton_raphson(f, df, x0, tol, max_iter)
% =========================================================================
% خوارزمية طريقة نيوتن رافسون (Newton-Raphson Method)
% مادة: التحليل العددي (Numerical Analysis)
% =========================================================================
% الوظيفة:
%   أشهر وأسرع الطرق المفتوحة ذات التقارب التربيعي (Quadratic Convergence)
%   لإيجاد جذور المعادلات غير الخطية f(x) = 0 باستخدام مماس المنحنى.
%
% صيغة التكرار:
%   x_{n+1} = x_n - [ f(x_n) / f'(x_n) ]
%
% المدخلات (Inputs):
%   f        : دالة المعادلة كـ function handle، مثال: @(x) x.^3 - x - 2
%   df       : دالة المشتقة الأولى f'(x)، مثال: @(x) 3*x.^2 - 1
%              (إذا تركت فارغة يتم حساب المشتقة عددياً بالفروق المركزية)
%   x0       : التخمين الابتدائي (افتراضياً: 1.5)
%   tol      : الدقة المطلوبة (افتراضياً: 1e-4)
%   max_iter : أقصى عدد تكرارات (افتراضياً: 50)
%
% المخرجات (Outputs):
%   root     : القيمة التقريبية للجذر المحسوب
%   T        : جدول التكرارات التفصيلي
% =========================================================================

    if nargin < 1 || isempty(f), f = @(x) x.^3 - x - 2; end
    if nargin < 2 || isempty(df), df = @(x) 3*x.^2 - 1; end
    if nargin < 3 || isempty(x0), x0 = 1.5; end
    if nargin < 4 || isempty(tol), tol = 1e-4; end
    if nargin < 5 || isempty(max_iter), max_iter = 50; end

    if ischar(f) || isstring(f), f = str2func(['@(x) ' char(f)]); end
    if ischar(df) || isstring(df), df = str2func(['@(x) ' char(df)]); end

    fprintf('\n=================================================================\n');
    fprintf('  طريقة نيوتن رافسون لحل المعادلات غير الخطية (Newton-Raphson)\n');
    fprintf('=================================================================\n');
    fprintf('التخمين الابتدائي: x0 = %.4f\n', x0);
    fprintf('الدقة المطلوبة: %e\n', tol);
    fprintf('-----------------------------------------------------------------\n');

    fprintf('%-4s | %-10s | %-11s | %-11s | %-10s | %-10s\n', ...
        'n', 'x_n', 'f(x_n)', 'f''(x_n)', 'x_{n+1}', 'الخطأ |x_{n+1}-x_n|');
    fprintf('-----------------------------------------------------------------\n');

    table_data = [];
    x_curr = x0;

    for n = 1:max_iter
        fx = f(x_curr);
        dfx = df(x_curr);

        if abs(dfx) < 1e-14
            error('خطأ: المشتقة الأولى f''(x_n) تساوي صفراً؛ المماس أفقي ولا يتقاطع مع محور السينات.');
        end

        % قانون نيوتن رافسون
        x_next = x_curr - (fx / dfx);
        err = abs(x_next - x_curr);

        fprintf('%-4d | %10.5f | %11.5f | %11.5f | %10.5f | %10.5e\n', ...
            n, x_curr, fx, dfx, x_next, err);

        table_data = [table_data; n, x_curr, fx, dfx, x_next, err]; %#ok<AGROW>

        if err < tol || abs(f(x_next)) < 1e-12
            fprintf('-----------------------------------------------------------------\n');
            fprintf('✓ تم الوصول للحل بنجاح فائق عند التكرار n = %d\n', n);
            fprintf('✓ الجذر التقريبي: x ≈ %.6f\n', x_next);
            fprintf('✓ قيمة الدالة عند الجذر: f(x) = %e\n', f(x_next));
            root = x_next;
            T = table_data;
            return;
        end

        x_curr = x_next;
    end

    root = x_curr;
    T = table_data;
    warning('تم بلوغ الحد الأقصى للتكرارات دون تحقيق الدقة المطلوبة.');
end
