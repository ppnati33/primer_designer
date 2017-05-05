from main.model.search_result import SearchResult


class TransformationHelper:

    @staticmethod
    def transform_results(search_results, search_results_wildcard):
        transformed_results = []
        # TODO: сделать добавление cut_positions в pattern сразу в процессе поиска
        for pattern, cut_positions in search_results.items():
            new_site = SearchResult(pattern.get_seq(), cut_positions)
            new_site.set_site_names(pattern.get_names())
            transformed_results.append(new_site)
        for pattern, cut_positions in search_results_wildcard.items():
            new_site = SearchResult(pattern.get_seq(), cut_positions)
            new_site.set_site_names(pattern.get_names())
            transformed_results.append(new_site)
        return transformed_results
