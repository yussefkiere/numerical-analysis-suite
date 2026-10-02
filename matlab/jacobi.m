function [x, T] = jacobi(A, b, x0, tol, max_iter)
% =========================================================================
% خوارزمية طريقة جاكوبي التكرارية (Jacobi Iterative Method)
% مادة: التحليل العددي (Numerical Analysis)
% =========================================================================
% الوظيفة:
%   حل نظام المعادلات الخطية A * x = b تكرارياً.
%   يشترط لتقارب الطريقة المحقق أن تكون مصفوفة المعاملات A مهيمنة قطرياً:
%   |a_{ii}| > sum_{j ~= i} |a_{ij}| لكل صف i
%
% قانون التكرار لجاكوبي:
%   x_i^{(k+1)} = [ b_i - sum_{j ~= i} (a_{ij} * x_j^{(k)}) ] / a_{ii}
%
% المدخلات (Inputs):
%   A        : مصفوفة المعاملات المربعة (n x n)
%   b        : متجه الثوابت (n x 1)
%   x0       : متجه التخمين الابتدائي (افتراضياً أصفار)
%   tol      : الدقة المطلوبة للتوقف (افتراضياً: 1e-4)
%   max_iter : أقصى عدد تكرارات (افتراضياً: 50)
%
% المخرجات (Outputs):
%   x : متجه الحل التقريبي النهائي
%   T : مصفوفة التكرارات وقيم الأخطاء
% =========================================================================

    if nargin < 1 || isempty(A)
        % مثال السبورة النموذجي للدكتور:
        % 8x1 +  x2 +  x3 = 26
        % 3x1 + 5x2 -  x3 = 7
        %  x1 -  x2 + 5x3 = 7
        A = [8,  1,  1; ...
             3,  5, -1; ...
             1, -1,  5];
    end
    if nargin < 2 || isempty(b)
        b = [26; 7; 7];
    end

    b = b(:);
    n = length(b);

    if nargin < 3 || isempty(x0), x0 = zeros(n, 1); end
    if nargin < 4 || isempty(tol), tol = 1e-4; end
    if nargin < 5 || isempty(max_iter), max_iter = 50; end

    x0 = x0(:);

    fprintf('\n=================================================================\n');
    fprintf('  طريقة جاكوبي التكرارية للأنظمة الخطية (Jacobi Iteration)\n');
    fprintf('=================================================================\n');

    % 1. فحص شرط الهيمنة القطرية الصارمة (Strict Diagonal Dominance)
    is_dominant = true;
    for i = 1:n
        diag_val = abs(A(i, i));
        row_sum = sum(abs(A(i, :))) - diag_val;
        fprintf('الصف %d: |a_%d%d| = %-4g | مجموع باقي الصف = %-4g', ...
            i, i, i, diag_val, row_sum);
        if diag_val > row_sum
            fprintf(' -> [محقق ✓]\n');
        else
            fprintf(' -> [غير محقق صراحة ⚠️]\n');
            is_dominant = false;
        end
    end

    if ~is_dominant
        warning('المصفوفة ليست مهيمنة قطرياً؛ قد لا تتقارب طريقة جاكوبي أو قد تحتاج لتبديل الصفوف.');
    else
        fprintf('✓ المصفوفة مهيمنة قطرياً بصرامة: التقارب مؤكد 100%%.\n');
    end

    fprintf('-----------------------------------------------------------------\n');

    % طباعة رأس الجدول
    header = sprintf('%-4s', 'k');
    for i = 1:n
        header = [header, sprintf(' | %-10s', sprintf('x%d', i))]; %#ok<AGROW>
    end
    header = [header, sprintf(' | %-10s', 'الخطأ ||x-x0||')];
    fprintf('%s\n', header);
    fprintf('-----------------------------------------------------------------\n');

    x_curr = x0;
    x_next = zeros(n, 1);
    table_data = [];

    % 2. حلقة التكرار
    for k = 1:max_iter
        for i = 1:n
            if abs(A(i, i)) < 1e-14
                error('خطأ: العنصر القطري A(%d,%d) يساوي صفراً؛ لا يمكن القسمة عليه.', i, i);
            end
            % طرح تأثير باقي المتغيرات من الطرف الأيمن
            sigma = A(i, :) * x_curr - A(i, i) * x_curr(i);
            x_next(i) = (b(i) - sigma) / A(i, i);
        end

        err = max(abs(x_next - x_curr)); % معيار اللانهاية للخطأ

        row_str = sprintf('%-4d', k);
        for i = 1:n
            row_str = [row_str, sprintf(' | %10.5f', x_next(i))]; %#ok<AGROW>
        end
        row_str = [row_str, sprintf(' | %10.5e', err)];
        fprintf('%s\n', row_str);

        table_data = [table_data; k, x_next', err]; %#ok<AGROW>

        if err < tol
            fprintf('-----------------------------------------------------------------\n');
            fprintf('✓ تقاربت طريقة جاكوبي بنجاح عند التكرار k = %d\n', k);
            for i = 1:n
                fprintf('  x%d = %.6f\n', i, x_next(i));
            end
            fprintf('✓ أقصى خطأ متبقي: %e\n', err);
            x = x_next;
            T = table_data;
            return;
        end

        x_curr = x_next;
    end

    x = x_next;
    T = table_data;
    warning('تم بلوغ الحد الأقصى للتكرارات دون تحقيق الدقة الكاملة.');
end
